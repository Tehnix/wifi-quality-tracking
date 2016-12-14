# WiFi Quality Tracking

A project for the Technical University of Denmark (DTU) to track WiFi quality across campus, using Raspberry Pis spread out across the university. The program:

- Measures WiFi quality
    - Signal Strength
    - Noise
    - Frequency in use
    - Round-trip times (RTT) to both campusnet.dtu.dk and to google.dk
    - Measures the DL/UL speeds using the `speedtest-cli` utility
- Periodically uploads the measurements to Dropbox


## Attribution

The project was originally made as a BSc project by Julia Loftsdottir, and then altered using the original code as inspiration and starting point.
