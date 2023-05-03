A summary of some things we know about the PixMob RF protocol as of 5/3/2023:
- Bracelets come in multiple frequencies based on region-specific rules. The ones in the USA work on 915 MHz. The PCBs are pretty much identical between frequency versions, except for the oscillator crystal. It remains to be seen if all it takes to convert signals between frequencies is to just shift the transmission frequency up or down; we will need to do that experiment.
- I was able to get some recordings with a Flipper device, uploaded here: https://drive.google.com/drive/u/0/folders/1_u44497iEh5vwa0nmH8oBaN2iDIis0Q3
- The protocol is based on OOK, with discrete time units of around 510 microseconds.
- I used a modified version of the raw IR parsing code from @Zach to translate them into binary by RLE, split out individual "codes", and produce "cleaner" versions by rounding the timings to what seems like the correct value. Those are in the "edited_rf_captures" folder.
- The bracelets have a very aggressive "sleeping" behavior, where they go into a sleep mode after only a few minutes of inactivity and have to be woken up by transmitting valid RF signals repeated for a while (up to 15-30 seconds?). The "nothing" code in Google Drive doesn't make the bracelets light up, but it does wake them up/keep them awake. It was transmitted a lot during the basketball game I was at, presumably to keep them ready for use at any given moment.
- There may well be another layer of encoding beyond just the RLE binary conversion, and probably some kind of CRC. 
- The FCC filing for the RF transmitter is here: https://fcc.report/FCC-ID/2ADS4-WAVENODE/. Page 4 of the internal photos (https://fcc.report/FCC-ID/2ADS4-WAVENODE/6178028) shows the RF module used for transmission to be a HopeRF RFM119W (https://www.hoperf.com/modules/rf_transmitter/RFM119.html).

I plan to do some brute-forcing with an Arduino and CC1101 module; I will post code here once that is done.

If you have any code, recordings, bracelet details, etc, please open a PR or Issue, or Discussion! You can also post in the Discord server: https://discord.gg/UYqTjC7xp3.
