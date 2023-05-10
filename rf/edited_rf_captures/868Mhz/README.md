These are modified RF commands,  based on the original files created by @danielweidman but have had the Frequency Changed from 915 Mhz to 868 Mhz to work with the EU/UK Version of the Pixmob WaveBands .

The original commands are some semi-manually created, cleaned, and spliced-out RF commands for the PixMob RF bracelets operating on 915 Mhz. 

The bracelets have a sleeping behavior that requires you to transmit a code repeatedly for up to ~30 seconds to "wake" them up after some time of inactivity. I reccomend using "nothing.sub" in the "withrepeats" folder for this purpose. After sending that for 30 seconds, the other codes will hopefully work.