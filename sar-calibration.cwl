$graph:
- baseCommand: sar-calibration
  class: CommandLineTool
  hints:
    DockerRequirement:
      dockerPull: mydocker
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
        LIB: aaaa
        PATH: /srv/conda/envs/env_sar_calibration/bin:/srv/conda/envs/env_sar_calibration/snap/bin:/srv/conda/envs/env_sar_calibration/bin:/srv/conda/condabin:/srv/conda/envs/env_sar_calibration/bin:/srv/conda/bin:/srv/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    ResourceRequirement:
      ramMin: 16000
  stderr: std.err
  stdout: std.out
- class: Workflow
  doc: help
  id: sar-calibration
  inputs:
    input_path:
      doc: help for input reference
      label: help for input reference
      type: Directory[]
  label: short help
  outputs:
  - id: wf_outputs
    outputSource:
    - step_1/results
    type:
      items: Directory
      type: array
  requirements:
  - class: ScatterFeatureRequirement
  steps:
    step_1:
      in:
        input_path: input_path
      out:
      - results
      run: '#clt'
      scatter: input_path
      scatterMethod: dotproduct
cwlVersion: v1.0
