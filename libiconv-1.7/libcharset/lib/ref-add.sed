/^# Packages using this file: / {
  s/# Packages using this file://
  ta
  :a
  s/ libcharset / libcharset /
  tb
  s/ $/ libcharset /
  :b
  s/^/# Packages using this file:/
}
