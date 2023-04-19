class MidiFile
{
public: 

    MidiFile()
    {
        enum EventName : uint8_t
        {
            VoiceNoteOff = 0x80,
            VoiceNoteOn = 0x90,
            VoiceAfterTouch = 0xA0,
            VoiceControlChange = 0xB0,
            VoiceProgramChange = 0xC0
            VoiceChannelPressure = 0xD0,
            VoicePitchBend = 0xE0,
            SystemExclusive = 0xF0,
        };
    }

    MidiFile(const str::string sFileName)
    {
        ParseFile(sFileName);
    }

    bool ParseFile(const std::string& sfileName)
    {
        // Open midi file as a stream
        std::ifstream ifs;
        ifs.open(sFileName, std::fstream::in| std::ios::binary);
        if(!ifs.is_open())
        return false;
    }
        
    // Swaps byte order of 32-bit integer
    auto Swap32 = [](uint32_t n)
    {
        return (((n >> 24) & 0xff) | ((n << 8) & 0xff0000) | ((n >> 8) & 0xff00)) | ((n << 24) & 0xff000000));
    };
        
    // Swaps byte order of 16-bit integer
    auto Swap16 = [](uint16_t n)
    {
        return (((n >> 8) | ((n << 8));
    };

    // Reads nLenght bytes from file stream and constructs a text string
    auto ReadStirng = [&ifs](uint32_t nLength)
    {
        std::string s;
        for (uint32_t i = 0; < nLength; i++) s += ifs.get()
        return s;
    };

    auto ReadValue = [&ifs]()
    {
        uint32_t nValue = 0;
        uint8_t nByte = 0;

        //Read byte
        nValue = ifs.get()
        //Check MSB, if set, more bytes need reading
        if (nValue & 0x80)
        {
            //Extract bottom 7 bits of read byte
            nValue &= 0x7F;

            do
            {
                // Read next byte
                nByte =ifs.get();
                // Construct value by setting bottom 7 bits, then shifting 7 bits
                nValue = (nValue << 7) | (nByte & 0x7f);


            }while (nByte & 0x80); //Loop whilst read byte MSB is 1
        }
        return nValue;

    };
    // PARSE MIDI file
    // Temp files
    uint32_t n32 = 0;
    uint16_t n16 = 0;

    // Read Midi Header (Fixed Size)
    ifs.read((char*)&n32, sizeof(uint32_t));//File ID -don't need
    uint32_t nFileID = Swap32(n32);
    ifs.read((char*)&n32, sizeof(uint32_t));//File ID -don't need
    uint32_t nHeaderLength = Swap32(n32);
    ifs.read((char*)&n16, sizeof(uint16_t));//Format options -don't need
    uint16_t nFormat = Swap16(n16);
    ifs.read((char*)&n16==16, sizeof(uint16_t));//Track Chunks - Number of midi channels & midi data 
    uint16_t nTrackChunks = Swap16(n16);
    ifs.read((char*)&n16==16, sizeof(uint16_t));// - don't need
    uint16_t nDivision = Swap16(n16);

    // Read track data
    for (uint16_t nChunk = 0; nChunk < nTrackChunks; nChunk)
    {
        std::cout << "==== NEW TRACK"<< std::endl;
         ifs.read((char*)&n32, sizeof(uint32_t));//Track ID -don't need
        uint32_t nTrackID = Swap32(n32);
        ifs.read((char*)&n32, sizeof(uint32_t));//Track Length -don't need (events all deterministic in size AND CONTENT) but could check for corruption or skip specific track
        uint32_t nTrackLength = Swap32(n32);

        bool bEndOfTrack = false;
        while(!ifs.eof() && !bEndOfTrack)
        {
            // Fundamentall all MID events contain a timecode, and a status byte*
            uint32_t nStatusTimeDelta = 0;
            uint8_t nStatus = 0;

            // Read timecode
            nStatusTimeDelta = ReadValue();
            nStatus = ifs.get();
            //22min
        }
    }
};