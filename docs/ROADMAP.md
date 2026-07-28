# Roadmap

This roadmap uses internal planning gates. They are not OpenAI program
requirements and do not guarantee acceptance into any support program.

## v0.1.0 — reproducible local slicing

- [x] Discover a user-installed Bambu Studio executable on macOS.
- [x] Probe Bambu Studio version and supported command-line options.
- [x] Produce a deterministic, shell-free slice plan.
- [x] Fingerprint source models with SHA-256.
- [ ] Execute an explicitly approved Bambu Studio slice in an isolated run
      directory.
- [ ] Capture duration, exit status, output hashes, and a redacted log.
- [ ] Add an OrcaSlicer execution adapter after local installation or a
      verified CI fixture is available.
- [ ] Publish at least ten redistributable test fixtures or generators.
- [ ] Complete at least one real Bambu printer validation.
- [ ] Publish the first stable release.

## v0.2.0 — regression comparison

- Compare two run manifests and classify changed inputs, settings, slicer
  versions, outputs, and timing.
- Define tolerances for stable numeric metrics.
- Generate a human-readable Markdown regression report.
- Package a privacy-reviewed upstream reproduction bundle.

## v0.3.0 — physical-print evidence

- Record printer model, nozzle, material, profile, environment, and measurement
  method without device serials.
- Attach photos and measurements by content hash.
- Link digital comparisons to physical observations.
- Publish a validation protocol and at least one repeatability study.

## Promotion gates

- [x] P0 public baseline draft prepared; publication requires account-owner
      confirmation.
- [ ] P1 first reproducible-slice evidence post.
- [ ] P2 v0.1.0 release announcement.
- [ ] P3 independent-use and maintainer-response update.

See [the promotion plan](PROMOTION.md) for evidence gates, cadence, privacy
rules, and internal measurement targets.
