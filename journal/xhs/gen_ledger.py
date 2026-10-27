#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 BOM.md 采购流水原表数据生成小红书长图 HTML（信息全保留）。
每行两条线：物品+金额 / 状态·店铺·规格·数量·订单号·物流
"""
import html, subprocess, os

ROWS = [
    # (日期, 订单号, 状态, 店铺, 物品, 规格, 数量, 金额, 物流)
    ("10-24 23:35", "5127890041090217248", "已付款", "深圳飞特舵机工厂店", "HD-1910-C001 调试板+线材", "FE-URT2-C001（重新下单，原 10-23 单已关闭）", "1", "45.00", "—"),
    ("10-24 23:35", "5127890041090080038", "已付款", "优利德自营官方店", "数字万用表（工具）", "UT136B+【+特尖表笔】", "1", "119.59", "—"),
    ("10-24 23:35", "5127890041090144411", "已付款", "树莓派零售商", "IMX219 160度摄像头", "IMX219 / 160° 广角（教程指定款）", "1", "60.00", "—"),
    ("10-24 23:35", "5127890041090099219", "已付款", "yaoyanzhutb的小店70", "外壳店家安装小工具包", "自行组装配套", "1", "19.90", "—"),
    ("10-24 23:35", "5127890041090108401", "待发货", "闪迪伯众专卖店", "microSD 卡 64G V10（一系统一备份）", "套餐四 + 官方标配各 1 张", "2", "194.80", "—"),
    ("10-24 23:35", "5127890041090171239", "待发货", "得力官方旗舰店", "线号标注：美纹纸胶带 + 油性记号笔", "20mm×20y 一卷；12 支混色双头", "各1", "20.90", "—"),
    ("10-24", "HenryIPforever", "已付款", "HenryIPforever（淘宝）", "Radxa ZERO 3W 主控 + 官方 8M 219 摄像头", "2GB RAM / 无 eMMC / 带排针（套餐）", "1套", "564.00", "—"),
    ("10-24", "团购（H906GO 付款）", "已付款", "飞特团购", "HD-1910 舵机（整机全套）", "¥95/个，一套 15 个", "15", "1425.00", "团购统一发货"),
    ("10-23 14:52", "5127828984003008018", "已发货", "yaoyanzhutb的小店70", "Microduck 3D 打印结构件（鸭子外壳）", "B 款 橙白 外壳（不含机械配件）；自行组装", "1", "159.00", "圆通 YT7651808622884"),

    ("10-22 21:18", "5127371355349180421", "已付款", "kissqy", "MicroDuck 官方套件 HAT", "HAT（成品，固件已烧）", "1", "119.00", "—"),
    ("10-22 21:18", "（同上订单）", "已付款", "kissqy", "MicroDuck 官方套件 IMU TO DXL", "IMU TO DXL（成品，固件已烧）", "1", "99.00", "—"),
    ("10-22 21:18", "5127371355349144411", "已发货", "都会明武电子", "VL53L5X V2 ToF 多区域激光测距", "VL53L5X V2 模块配盖片", "1", "49.50", "中通 79042017251844"),
    ("10-22 21:18", "5127371355349008018", "已发货", "fb数码旗舰店", "NP-F550 锂电池（整机电源）", "2200mAh 2 电 + 标准双充套装", "1", "82.00", "—"),
    ("10-22 21:18", "5127371355349280804", "已发货", "优可吉轴承销售店", "6700 开式薄壁轴承", "10×15×3mm 轴承钢", "5", "10.00", "中通 79041990445590"),
    ("10-22 21:18", "（同上订单）", "已发货", "优可吉轴承销售店", "ET2216 超薄壁轴承", "16×22×4mm 轴承钢", "12", "36.00", "中通 79041990445590"),
    ("10-22 21:18", "5127371355349362823", "已发货", "永茂电子", "AMP2.0-3P 舵机线 100mm", "1007/24#；双头反向；AMP2.0-3P", "30", "45.00", "申通 773448070959273"),
    ("10-22 21:18", "（同上订单）", "已发货", "永茂电子", "AMP2.0-3P 舵机线 200mm", "1007/24#；双头反向；AMP2.0-3P", "30", "60.00", "申通 773448070959273（订单含运费 8，实付 113）"),
    ("10-22 21:18", "5127371355349017200", "已发货", "固万基官方旗舰店", "自攻螺丝 M2×4 镀镍", "200 只装", "1", "1.99", "圆通 YT7651599182057"),
    ("10-22 21:18", "（同上订单）", "已发货", "固万基官方旗舰店", "自攻螺丝 M2×5 镀镍", "200 只装", "1", "2.11", "圆通 YT7651599182057"),
    ("10-22 21:18", "（同上订单）", "已发货", "固万基官方旗舰店", "自攻螺丝 M2×6 镀镍", "200 只装", "1", "2.17", "圆通 YT7651599182057"),
    ("10-22 21:18", "（同上订单）", "已发货", "固万基官方旗舰店", "自攻螺丝 M2×8 镀镍", "200 只装", "1", "2.35", "圆通 YT7651599182057"),
    ("10-22 21:18", "（同上订单）", "已发货", "固万基官方旗舰店", "自攻螺丝 M2×12 镀镍", "200 只装", "1", "2.55", "圆通 YT7651599182057"),
    ("10-22 21:18", "（同上订单）", "已发货", "固万基官方旗舰店", "自攻螺丝 M2.6×8 镀镍", "200 只装", "1", "2.36", "圆通 YT7651599182057"),
    ("10-22 21:18", "5127371355349226430", "已发货", "启色数码旗舰店", "EH2.5MM 3P 胶壳", "50 个装", "1", "2.80", "圆通 YT7651591427121"),
    ("10-22 21:18", "（同上订单）", "已发货", "启色数码旗舰店", "EH2.5MM 2P 胶壳", "50 个装", "1", "2.20", "圆通 YT7651591427121"),
    ("10-22 21:18", "（同上订单）", "已发货", "启色数码旗舰店", "EH2.5MM 端子", "100 个装", "1", "3.50", "圆通 YT7651591427121"),
    ("10-22 21:18", "5127371355349171239", "已发货", "萨牛旗舰店", "特软硅胶排线 3 芯 22AWG", "黑色；1m/条", "3", "12.60", "申通 773447974734042"),
    ("10-22 21:18", "5127371355349326813", "已发货", "信容芯旗舰店", "SH1.0 转杜邦母线 4P", "0.2m；1.0-4P 转杜邦母", "5条", "4.80", "圆通 YT7651648598712"),
    ("10-22 21:18", "5127371355349353641", "已发货", "优信电子", "3525 腔体扬声器（音效）", "4Ω 3W，带 1.25 端子", "1", "2.77", "圆通 YT7651581021601"),
    ("10-22 21:18", "5127371355349135229", "已发货", "圣佰路旗舰店", "热缩管套装（绝缘保护）", "164 片 彩色 2 倍收缩", "1", "3.05", "申通 773447973173515"),
    ("10-22 21:18", "5127371355349418014", "已发货", "渡竹旗舰店", "特软耐高温硅胶线 22AWG", "黑色 2m", "1", "3.45", "申通 773447973727455"),
    ("10-22 21:18", "5127371355349444842", "已发货", "安立信旗舰店", "电烙铁恒温焊台（工具）", "937A 升级数显 套餐二", "1", "104.14", "申通 773448004394308"),
]

GROUPS = [
    ("采购流水 · 原样收录 ①", "10 月 24 日下单（含 23:35 批次）", ROWS[0:9], "Part 2 / 5", ""),
    ("采购流水 · 原样收录 ②", "10 月 22 日 21:18 批次（核心件）", ROWS[9:20], "Part 3 / 5", ""),
    ("采购流水 · 原样收录 ③", "10 月 22 日 21:18 批次（小件与工具）", ROWS[20:32], "Part 4 / 5",
     "共 32 行明细，已剔除「交易关闭」的重复下单批次与非项目订单（童装、生活用品等）"),
]

TPL = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1440px;overflow:hidden;font-family:"PingFang SC","Hiragino Sans GB",sans-serif;
background:#FDF6EC;color:#1F1D1B;padding:44px 40px 32px;display:flex;flex-direction:column}}
.head{{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:6px}}
h1{{font-size:40px;font-weight:800;letter-spacing:-.5px;line-height:1.2}}
h1 em{{font-style:normal;color:#E8722C}}
.sub{{font-size:20px;color:#9A9188;margin-top:8px}}
.tag{{font-size:18px;color:#B3A99E;letter-spacing:2px;padding-bottom:6px}}
table{{width:100%;border-collapse:collapse;margin-top:14px;background:#fff;border-radius:18px;overflow:hidden;
box-shadow:0 8px 26px rgba(180,140,90,.12)}}
tr{{border-bottom:1px solid #F3EEE6}}
tr:last-child{{border-bottom:none}}
tr:nth-child(even){{background:#FDFBF7}}
td{{padding:9px 14px}}
.name{{font-size:21px;font-weight:700;letter-spacing:-.2px}}
.meta{{font-size:15px;color:#A0968C;margin-top:4px;line-height:1.45}}
.meta b{{color:#C4763A;font-weight:600}}
.amt{{text-align:right;font-size:23px;font-weight:800;letter-spacing:-.5px;white-space:nowrap;font-variant-numeric:tabular-nums}}
.note{{margin-top:12px;font-size:17px;color:#A79E94;line-height:1.5}}
.foot{{margin-top:auto;display:flex;justify-content:space-between;align-items:center;
background:#1F1D1B;color:#fff;border-radius:16px;padding:16px 24px;font-size:18px;color:#C9C2BA;letter-spacing:.5px}}
.foot b{{color:#FFC078;font-size:26px;font-weight:800;letter-spacing:-.5px}}
</style></head><body>
<div class="head"><div><h1>{title}<br><em>{subtitle}</em></h1></div><div class="tag">{tag}</div></div>
<table>{rows}</table>
{note}
<div class="foot"><span>数据源：项目 BOM.md 采购流水原表 · 金额为实付</span><span><b>{foot}</b></span></div>
</body></html>"""


def mask_digits(s: str, keep_head=6, keep_tail=4) -> str:
    """对长数字串打码：保留头尾，中间用 * 替换。非纯数字（如团购/店铺名）原样返回。"""
    if not s.isdigit() or len(s) <= keep_head + keep_tail:
        return s
    return s[:keep_head] + "*" * (len(s) - keep_head - keep_tail) + s[-keep_tail:]


def mask_tracking(s: str) -> str:
    """物流单号打码：保留快递公司名与单号头尾。"""
    parts = s.split(" ")
    out = []
    for p in parts:
        if len(p) >= 8 and any(c.isdigit() for c in p):
            out.append(p[:4] + "*" * max(0, len(p) - 8) + p[-4:])
        else:
            out.append(p)
    return " ".join(out)


def row_html(r):
    date, oid, status, shop, item, spec, qty, amt, logi = r
    flag = "🟢" if status == "已付款" else ("📦" if status == "已发货" else "🚚")
    return (
        "<tr><td>"
        f'<div class="name">{item}</div>'
        f'<div class="meta">{flag} {status} · <b>{shop}</b> · {spec} · ×{qty}<br>'
        f'订单 {mask_digits(oid)} · 物流 {mask_tracking(logi)} · 下单 {date}</div>'
        "</td>"
        f'<td class="amt">¥{amt}</td></tr>'
    )


os.chdir(os.path.dirname(os.path.abspath(__file__)))
for idx, (title, subtitle, rows, tag, note) in enumerate(GROUPS, start=6):
    body = "".join(row_html(r) for r in rows)
    note_html = f'<div class="note">{note}</div>' if note else ""
    foot = "共 32 行" if idx == 8 else f"{len(rows)} 行"
    out = TPL.format(title=title, subtitle=subtitle, tag=tag, rows=body, note=note_html, foot=foot)
    fn = f"card{idx}.html"
    with open(fn, "w", encoding="utf-8") as f:
        f.write(out)
    subprocess.run([
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=2", "--window-size=1080,1440",
        f"--screenshot=card{idx}.png", f"file://{os.path.abspath(fn)}",
    ], capture_output=True)
    print("rendered", fn, len(rows), "rows")
