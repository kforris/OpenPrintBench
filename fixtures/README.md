# Redistributable fixtures

`cube-20mm.stl` is an original, deterministic ASCII STL created for
OpenPrintBench. It contains a 20 mm cube represented by 12 triangles and is
dedicated to the public domain under CC0-1.0. Its adjacent `.license` file is
the authoritative redistribution notice.

For an evidence run, pin the fixture to the full Git commit that contains the
exact bytes and use:

- source URL:
  `https://github.com/kforris/OpenPrintBench/blob/<commit>/fixtures/cube-20mm.stl`
- source commit: the same full 40-character Git SHA;
- license: `CC0-1.0`;
- input SHA-256: calculated by OpenPrintBench at execution time.

The fixture is digital test geometry only. Its presence does not imply that a
slice has run or that a physical print has been validated.
