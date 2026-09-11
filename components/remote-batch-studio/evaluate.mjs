import { promises as fs } from "node:fs";
import path from "node:path";
import { readState, updateState, toolRoot } from "./lib/store.mjs";

const STEP_API_KEY = process.env.STEP_API_KEY;
const EVAL_MODEL = process.env.STEP_EVAL_MODEL ?? "step-3.7-flash";
const API_URL = process.env.STEP_CHAT_URL ?? "https://api.stepfun.com/step_plan/v1/chat/completions";
const ROOT = toolRoot();
const REPORT_PATH = path.join(ROOT, "data", "evaluation-report.md");

const SYSTEM_PROMPT = `你在评估一张 AI 生成的图是否符合原始提示词。
只返回一个 JSON 对象，不要任何额外文字、不要 markdown 围栏。
格式：
{
  "verdict": "match" | "partial" | "mismatch",
  "score": 0 到 100 的整数,
  "summary": "一句话总结图与提示词的吻合情况",
  "deviations": ["具体偏差点1", "偏差点2"]
}
评分规则：
- 90-100 完美匹配，所有关键元素都在
- 70-89 大致符合，有次要元素缺失或偏差
- 50-69 主体对但有明显错误
- 0-49 完全跑偏或主题错误
deviations 没有偏差就返回空数组 []。`;

function buildBody(prompt, imageUrl) {
  return {
    model: EVAL_MODEL,
    messages: [
      { role: "system", content: SYSTEM_PROMPT },
      {
        role: "user",
        content: [
          { type: "text", text: `原始提示词:\n${prompt}` },
          { type: "image_url", image_url: { url: imageUrl } },
        ],
      },
    ],
    response_format: { type: "json_object" },
    temperature: 0,
  };
}

function parseJsonLoose(text) {
  try {
    return JSON.parse(text);
  } catch {
    const match = text.match(/\{[\s\S]*\}/);
    if (match) {
      try {
        return JSON.parse(match[0]);
      } catch {
        return null;
      }
    }
    return null;
  }
}

const FIELD_ALIASES = [
  ["verdict", ["verdict", "result", "rating", "judgement"]],
  ["score", ["score", "points", "rating"]],
  ["summary", ["summary", "comment", "description", "conclusion"]],
  ["deviations", ["deviation", "issue", "gap", "diff"]],
];

function normalizeEvaluation(raw) {
  if (!raw || typeof raw !== "object") return null;
  const out = {};

  for (const [target, aliases] of FIELD_ALIASES) {
    for (const [key, value] of Object.entries(raw)) {
      const cleaned = String(key).replace(/[^a-zA-Z]/g, "").toLowerCase();
      if (!cleaned) continue;
      if (aliases.some((alias) => cleaned.includes(alias))) {
        if (out[target] === undefined) out[target] = value;
        break;
      }
    }
  }

  if (typeof raw === "object") {
    const stringValues = Object.values(raw).filter((v) => typeof v === "string");
    if (!out.verdict && stringValues.length === 1) {
      const v = stringValues[0].toLowerCase();
      if (["match", "partial", "mismatch"].includes(v)) out.verdict = v;
    }
  }

  if (typeof out.score === "string") out.score = Number(out.score) || 0;
  if (!out.verdict && typeof out.score === "number") {
    out.verdict = out.score >= 90 ? "match" : out.score >= 50 ? "partial" : "mismatch";
  }
  if (out.score === undefined && out.verdict) {
    out.score = out.verdict === "match" ? 90 : out.verdict === "partial" ? 60 : 20;
  }
  if (!out.verdict) out.verdict = "mismatch";
  if (out.score === undefined) out.score = 0;
  if (!Array.isArray(out.deviations)) {
    out.deviations = out.deviations ? [String(out.deviations)] : [];
  }
  return out;
}

async function evaluateOne(asset, retries = 2) {
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const r = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${STEP_API_KEY}`,
        },
        body: JSON.stringify(buildBody(asset.prompt, asset.resultUrl)),
      });
      const text = await r.text();
      if (!r.ok) {
        throw new Error(`HTTP ${r.status}: ${text.slice(0, 200)}`);
      }
      const data = JSON.parse(text);
      const content = data?.choices?.[0]?.message?.content;
      if (!content) {
        throw new Error("empty content");
      }
      const parsed = normalizeEvaluation(parseJsonLoose(content));
      if (!parsed) {
        throw new Error(`cannot parse JSON: ${content.slice(0, 200)}`);
      }
      return parsed;
    } catch (err) {
      if (attempt === retries) {
        return { error: err.message };
      }
      await new Promise((r) => setTimeout(r, 1000 * (attempt + 1)));
    }
  }
}

function pad(str, len) {
  const s = String(str ?? "");
  return s.length > len ? s.slice(0, len - 1) + "…" : s.padEnd(len);
}

async function main() {
  if (!STEP_API_KEY) {
    console.error("Missing env STEP_API_KEY");
    process.exit(1);
  }

  const args = process.argv.slice(2);
  const force = args.includes("--force");
  const targetBatchId = args.find((a) => !a.startsWith("--"));

  const state = await readState();

  let batchesToShow = state.batches;
  if (targetBatchId) {
    batchesToShow = state.batches.filter((b) => b.id === targetBatchId || b.name === targetBatchId);
    if (batchesToShow.length === 0) {
      console.error(`找不到批次: ${targetBatchId}`);
      process.exit(1);
    }
  }

  const batchIds = new Set(batchesToShow.map((b) => b.id));
  let assets = state.assets.filter(
    (a) => batchIds.has(a.batchId) && a.status === "completed" && a.resultUrl,
  );
  if (!force) {
    assets = assets.filter((a) => !a.evaluation);
  }

  if (assets.length === 0) {
    console.log("没有可评估的图（已评估过的跳过，加 --force 重评）。");
    return;
  }

  console.log(`评估 ${assets.length} 张，模型 ${EVAL_MODEL}…\n`);

  const rows = [];
  for (const asset of assets) {
    process.stdout.write(`  [${asset.promptIndex}] ${asset.prompt.slice(0, 30)}… → `);
    const result = await evaluateOne(asset);
    if (result.error) {
      console.log("ERROR");
      rows.push({ asset, error: result.error });
      continue;
    }
    await updateState((draft) => {
      const target = draft.assets.find((a) => a.id === asset.id);
      if (target) {
        target.evaluation = {
          ...result,
          model: EVAL_MODEL,
          evaluatedAt: new Date().toISOString(),
        };
      }
      return draft;
    });
    console.log(`${result.score} ${result.verdict}`);
    rows.push({ asset, result });
  }

  console.log("\n" + "─".repeat(80));
  console.log(pad("#", 4) + pad("SCORE", 7) + pad("VERDICT", 9) + pad("SUMMARY", 50));
  console.log("─".repeat(80));
  for (const row of rows) {
    if (row.error) {
      console.log(pad(`[${row.asset.promptIndex}]`, 4) + "ERROR: " + row.error);
      continue;
    }
    const r = row.result;
    console.log(
      pad(`[${row.asset.promptIndex}]`, 4) +
        pad(String(r.score), 7) +
        pad(r.verdict, 9) +
        pad(r.summary, 50),
    );
    if (Array.isArray(r.deviations) && r.deviations.length) {
      for (const d of r.deviations) {
        console.log("    • " + d);
      }
    }
  }
  console.log("─".repeat(80));

  const scored = rows
    .filter((r) => r.result && typeof r.result.score === "number")
    .map((r) => r.result.score);
  if (scored.length) {
    const avg = (scored.reduce((a, b) => a + b, 0) / scored.length).toFixed(1);
    const matchCount = rows.filter((r) => r.result?.verdict === "match").length;
    const mismatchCount = rows.filter((r) => r.result?.verdict === "mismatch").length;
    console.log(
      `平均分 ${avg} | 完美 ${matchCount} | 跑偏 ${mismatchCount} | 共 ${scored.length}`,
    );
  }

  const report = renderReport(batchesToShow, state, rows);
  await fs.writeFile(REPORT_PATH, report, "utf8");
  console.log(`\n报告已写入: ${REPORT_PATH}`);
}

function renderReport(batches, state, rows) {
  const lines = [];
  lines.push(`# 评估报告`);
  lines.push("");
  lines.push(`生成时间：${new Date().toISOString()}`);
  lines.push(`评估模型：${EVAL_MODEL}`);
  lines.push("");

  const byBatch = new Map();
  for (const row of rows) {
    const b = state.batches.find((x) => x.id === row.asset.batchId);
    const key = b?.name ?? row.asset.batchId;
    if (!byBatch.has(key)) byBatch.set(key, []);
    byBatch.get(key).push(row);
  }

  for (const [batchName, batchRows] of byBatch) {
    lines.push(`## ${batchName}`);
    lines.push("");
    const scored = batchRows.filter((r) => r.result).map((r) => r.result.score);
    if (scored.length) {
      const avg = (scored.reduce((a, b) => a + b, 0) / scored.length).toFixed(1);
      lines.push(`- 共 ${batchRows.length} 张，平均分 ${avg}`);
      lines.push("");
    }
    for (const row of batchRows) {
      lines.push(`### [${row.asset.promptIndex}] ${row.asset.prompt}`);
      lines.push("");
      if (row.error) {
        lines.push(`**评估失败**：${row.error}`);
        lines.push("");
        continue;
      }
      const r = row.result;
      const emoji = r.verdict === "match" ? "✅" : r.verdict === "partial" ? "⚠️" : "❌";
      lines.push(`${emoji} **${r.verdict}** · 得分 **${r.score}**`);
      lines.push("");
      if (r.summary) {
        lines.push(`> ${r.summary}`);
        lines.push("");
      }
      if (Array.isArray(r.deviations) && r.deviations.length) {
        lines.push(`偏差点：`);
        for (const d of r.deviations) lines.push(`- ${d}`);
        lines.push("");
      }
      if (row.asset.resultUrl) {
        lines.push(`[图片链接](${row.asset.resultUrl})`);
        lines.push("");
      }
    }
  }
  return lines.join("\n");
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
