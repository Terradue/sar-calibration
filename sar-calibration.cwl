$graph:
- baseCommand: sar-calibration
  class: CommandLineTool
  id: clt
  inputs:
    input_path:
      inputBinding:
        position: 1
        prefix: --input_path
      type: Directory
    aoi:
      inputBinding:
        position: 2
        prefix: --aoi
      type: string
  outputs:
    results:
      outputBinding:
        glob: .
      type: Directory
  requirements:
    EnvVarRequirement:
      envDef:
        PATH: /srv/conda/envs/env_sar_calibration/bin:/srv/conda/envs/env_sar_calibration/bin:/srv/conda/condabin:/srv/conda/envs/env_sar_calibration/bin:/srv/conda/bin:/srv/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    ResourceRequirement: {}
  stderr: std.err
  stdout: std.out
- class: Workflow
  doc: help
  id: sar-calibration
  inputs:
    input_path:
      doc: help for input reference
      label: help for input reference
      type: Directory
    aoi:
      doc: help for the area of interest
      label: help for the area of interest
      type: string
  label: short help
  outputs:
  - id: wf_outputs
    outputSource:
    - step_1/results
    type: Directory
  steps:
    step_1:
      in:
        input_path: input_path
        aoi: aoi
      out:
      - results
      run: '#clt'
cwlVersion: v1.0
