# Bambu STL repeatability evidence — 2026-07-28

This record covers two local, explicitly approved digital slicing runs. It
does not claim a physical print, printer control, cloud access, or hardware
validation.

## Provenance

- OpenPrintBench fixture commit:
  `2d2c54e9d9ddc53a365606b9d9d070b94caeb64c`
- Fixture: `fixtures/cube-20mm.stl`, project-authored, `CC0-1.0`
- Fixture SHA-256:
  `369c23daac96f4cde40ec6a0e13afb9be5ec4cbbf974c071c60f1009824477c4`
- Fixture size: `1517` bytes
- Slicer: Bambu Studio `02.06.00.51`
- Installed profile source commit:
  `b506005bc4ee62124e24bf00e0f58656db3646a6`
- Installed profile source license: `AGPL-3.0-only`
- Materializer: `openprintbench-bambu-profile-merge-v1`
- Machine: `Bambu Lab X1 Carbon 0.4 nozzle.json`
- Process: `0.20mm Standard @BBL X1C.json`
- Filament: `Generic PLA.json`

The selected profile files were used only as local inputs. Their inheritance
was materialized into the isolated run directory; neither those profiles nor
generated 3MF/G-code files are stored in this repository.

## Captured development attempts

Before the two successful runs, the executor captured two non-success states
without producing output files:

- Installed leaf profiles were passed directly: duration `0.278480` seconds,
  exit status `-11` (signal 11), redacted log SHA-256
  `f1de4e2a8b778b70ef41d56836046f5e73b8e07aa756e46471a11e3850dcc3fc`.
  This led to the complete-profile materializer.
- Materialized profiles were used with an incomplete orientation argument:
  duration `0.070092` seconds, exit status `254`, redacted log SHA-256
  `5a9942777f3bb22d04188093b67f318b551a4b09ad90b9430f289b1aeb410a8d`.
  The argument was corrected to the documented `--orient 1` form.

Both manifests retained `physical_validation: null`.

## Run results

| Field | Run 1 | Run 2 | Classification |
| --- | --- | --- | --- |
| Exit status | `0` | `0` | stable |
| Timed out | `false` | `false` | stable |
| Duration (seconds) | `0.650262` | `0.472667` | expected variable |
| G-code size (bytes) | `278335` | `278335` | stable |
| G-code SHA-256 | `f6c6365d65ecf1110f4aefd1097558378006ad4f1738648fba74c0bfa95205c5` | same | stable |
| 3MF size (bytes) | `55621` | `55621` | stable |
| 3MF SHA-256 | `57ce07f1176c466cd20a97908038a5c3a8d167937eec796544bb73750d0d3c9d` | `146dcd84ea9ed468ca52abc8e8149d1d44b4310445dd341d71aa9b126f6bab31` | variable container bytes |
| `result.json` SHA-256 | `d97fc5b7900c937e64bfb114a26089fa0196ec79dbfbb7210147baed2dbcb547` | `17cee9b309239fe0dc6a74681a76f73ca936f58e1aec10d53047a1ccdf591e23` | variable timing fields |
| Redacted log SHA-256 | `5d701094d4e0cd5535a456dd9c28b1923070f83a007eeee9b055e0e59c41429e` | `25fa3d3424d53cddee09f9dd3a0330000908a9fd6d01b9be5956b1c3586f3550` | variable timestamps |
| Physical validation | `null` | `null` | not performed |

## Stable inputs and settings

The portable command array, fixture hash, slicer version, source profile
hashes, materialized profile hashes, output names, approval state, and exit
status matched across both runs. In particular:

- materialized machine SHA-256:
  `b5a60ef9b156acce52fa5b083595af1a00d7c478ccdc05f1b7f4e59b5e6c6a7b`
- materialized process SHA-256:
  `5d6ec0717d02b0293d45798d3c776d141e6a3f03876ee519863028de6b992039`
- materialized filament SHA-256:
  `2ee424b81096dbdf4f6c8e09a7f7f46a840a5b44fa857db19c290871ff2c67b8`

The differing `result.json` fields were execution-time measurements such as
`export_time`, `prepare_time`, perimeter/infill time, and total sliced time.
The redacted logs differed at timestamp positions. The matching G-code hash is
the strongest byte-level repeatability result from these two runs; the varying
3MF container hash must not be treated as a slicing regression by itself.
