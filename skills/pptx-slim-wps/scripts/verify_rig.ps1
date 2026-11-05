# WPS slideshow ground-truth capture rig (non-invasive, proven rig11/12 pattern).
# Usage: powershell -File verify_rig.ps1 <deck.pptx ASCII path> <outdir> <slide1,slide2,...> [tag]
# Parks the slideshow window bottom-right (no focus steal), captures 2 frames per slide
# 1.5s apart. Judge animation by pixel diff of the media region (>10% = animating).
# Rules: never PrintWindow on occluded windows (DWM frozen cache = false negative);
# never SetCursorPos/mouse_event while user is on the machine.
param($deck, $outdir, $slidesCsv, $tag = 'v')
$ErrorActionPreference = 'Continue'
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class RV {
    public delegate bool EnumProc(IntPtr hWnd, IntPtr lParam);
    [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr lp);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
    [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h, IntPtr after, int x, int y, int cx, int cy, uint flags);
    [DllImport("user32.dll")] public static extern int GetSystemMetrics(int n);
    [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
}
"@
function FindShowWindow {
    $procs = @(Get-Process | Where-Object { $_.Name -match 'wpp|kwpp|wps' } | Select-Object -ExpandProperty ID)
    $found = New-Object System.Collections.ArrayList
    $cb = {
        param($h, $lp)
        $pid2 = 0
        [RV]::GetWindowThreadProcessId($h, [ref]$pid2) | Out-Null
        if ($procs -contains [int]$pid2 -and [RV]::IsWindowVisible($h)) {
            $r = New-Object RV+RECT
            [RV]::GetWindowRect($h, [ref]$r) | Out-Null
            $w = $r.R - $r.L; $ht = $r.B - $r.T
            if ($w -gt 800 -and $ht -gt 600) { $found.Add("$h") | Out-Null }
        }
        return $true
    }
    [RV]::EnumWindows($cb, [IntPtr]::Zero) | Out-Null
    if ($found.Count -eq 0) { return [IntPtr]::Zero }
    return [IntPtr]::new([int64]($found[0]))
}
$cap = {
    param($h, $path)
    $r = New-Object RV+RECT
    [RV]::GetWindowRect($h, [ref]$r) | Out-Null
    $w = $r.R - $r.L; $ht = $r.B - $r.T
    $bmp = New-Object Drawing.Bitmap($w, $ht)
    $g = [Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($r.L, $r.T, 0, 0, (New-Object Drawing.Size($w, $ht)))
    $g.Dispose(); $bmp.Save($path); $bmp.Dispose()
}
$vw = [RV]::GetSystemMetrics(78); $vh = [RV]::GetSystemMetrics(79)
$app = New-Object -ComObject Kwpp.Application
$p = $app.Presentations.Open($deck, $true, $false, $true)
$win = $p.SlideShowSettings.Run()
Start-Sleep -Milliseconds 1500
$h = FindShowWindow
if ($h -eq [IntPtr]::Zero) { Write-Host 'NO SHOW WINDOW'; exit 1 }
$x = [Math]::Max(0, $vw - 740); $y = [Math]::Max(0, $vh - 520)
[RV]::SetWindowPos($h, [IntPtr]::Zero, $x, $y, 720, 450, 0x0010 -bor 0x0200 -bor 0x0400) | Out-Null
Start-Sleep -Milliseconds 800
foreach ($s in $slidesCsv.Split(',')) {
    $win.View.GotoSlide([int]$s)
    Start-Sleep -Milliseconds 600
    try { Write-Host ("s$s idx=" + $win.View.Slide.SlideIndex + " id=" + $win.View.Slide.SlideID) }
    catch { Write-Host "s$s idx FAIL"; continue }
    Start-Sleep -Milliseconds 1200
    & $cap $h "$outdir\${tag}s${s}_1.png"
    Start-Sleep -Milliseconds 1500
    & $cap $h "$outdir\${tag}s${s}_2.png"
}
try { $win.View.Exit() } catch {}
$p.Close()
$app.Quit()
Write-Host 'RIG DONE'
