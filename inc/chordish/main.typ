#import "@preview/chordish:0.2.3": songbook
#show: songbook.with(
  instrument: "guitar",
  chords: "above",
  diagrams: true,
  autochord: true
)

#text(size: 24pt)[*Example Songbook*]
#outline(depth: 1)

#include "songs/Example Song.typ"
