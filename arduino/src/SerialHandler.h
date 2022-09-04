//header file with the SerialHandler class
#ifndef SerialHandler_h
#define SerialHandler_h

class SerialHandler {
    
    private:
    
    public:
        SerialHandler(uint8_t rx, uint8_t tx);
        void update();
};

#endif