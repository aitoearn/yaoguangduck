# Duck 复刻项目

> 开始日期：2026-10-24
> 目标：复刻 Duck（开源四足/机器鸭项目），完整记录设计→采购→组装→训练全过程

## 目录结构

| 路径 | 内容 | 更新方式 |
|---|---|---|
| `design/SOLUTION.md` | 方案设计（总体架构、技术路线） | 持续更新 |
| `design/DECISIONS.md` | 关键决策记录（选型理由、备选对比） | 追加 |
| `procurement/BOM.md` | 材料清单与购买记录 | 追加 |
| `build/ASSEMBLY-LOG.md` | 组装过程日志 | 按日期追加 |
| `build/LESSONS.md` | 经验与踩坑记录 | 追加 |
| `software/TRAINING-LOG.md` | 软件与训练日志（环境、参数、结果） | 按日期追加 |
| `journal/` | 每日流水日志 | 按日期追加 |

## 使用方式

- 对话中说"记一下：xxx" → 记录到对应文件
- 阶段性说"保存/整理" → 把流水提炼进主题文档
- 重大决策先记 DECISIONS.md，防止事后想不起来为什么这么选

## 当前状态

- [x] 方案设计（M1 冻结，见 design/SOLUTION.md）
- [x] 材料采购（大件全齐，小件组装时按需补买；总投入约 ¥3263）
- [ ] 组装（等货中；到货后从 M3 刷机验证开始）
- [ ] 软件训练
- [ ] 联调跑通

## 参考资料

- 原项目：Pollen Robotics Microduck（官方整机 $399）
- 复刻主线仓库：kissqy/Microduck-kissqy（本地克隆：/Users/lisq/project/jiqiren/Microduck-kissqy）
- 复刻教程（本地整理版）：/Users/lisq/project/jiqiren/MicroDuck复刻教程.md（2026-10-22 版）
- 3D 打印件（缝合怪版，备用）：仓库 hardware/3d-print-frankenduck/（36 STL）
