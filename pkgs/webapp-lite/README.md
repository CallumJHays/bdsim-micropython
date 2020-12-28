# `bdsim.webapp-lite`

Webapp Telemetry tuner implementation with static layout. Designed for minimized bundle size, for resource-limited micropython devices with potentially no connection to the greater internet (such as a mobile robot accessible via self-hosted WiFi hotspot).

The web-client will check for an internet connection at runtime in the browser. If so this will switch to the more feature-full `bdsim.webapp-full`.
