# Throughput
- Components
  - automatic-wannier-flow
  - cryspy
  - Others
    - seek_parh
  - Future
    - Evaluation
      - pbctools etc
    - LatticeModel GCN
#### TODO
- awf: VASP-->QE
- awf: VASP使用権限
#### 自作auto-wannier-flow
- 手順(例:FeSe)
  - QEでscf計算
  - QEでdos計算
  - 重要軌道を決め打ちする(概ね事前知識でできる)
    - FeSeの場合Feの3d軌道
    - TMTTFの場合Cの2p,Sの3p軌道
  - dosから重要軌道の密度が高いwindow作成
  - respackインプット作成してwannier計算
