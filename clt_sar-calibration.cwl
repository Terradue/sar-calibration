baseCommand: sar-calibration
class: CommandLineTool
cwlVersion: v1.0
id: clt
inputs:
  input_path:
    inputBinding:
      position: 1
      prefix: --input_path
    type: Directory
outputs:
  results:
    outputBinding:
      glob: .
    type: Directory
requirements:
  EnvVarRequirement:
    envDef:
      PATH: /srv/conda/envs/env_sar_calibration/bin:/srv/conda/envs/env_sar_calibration/snap/bin:/srv/conda/envs/env_sar_calibration/bin:/srv/conda/condabin:/srv/conda/envs/env_sar_calibration/bin:/srv/conda/bin:/srv/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
  ResourceRequirement: {}
stderr: std.err
stdout: std.out
