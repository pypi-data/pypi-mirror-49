//
// Created by fancy on 2019/6/20.
//

#include <cstring>
#include <cstdlib>
#include <iostream>
#include "genstr.h"
#include <ctime>
#include <random>

void inline initRand() {
    /* Initializes random number generator */
    srand((unsigned) time(nullptr));
}
void feed(char *subBuf, int len) {
    unsigned int r = rand();
    for(int i=0;i<len;i++){
        while((r & 0xff) ==0) {
            r = r >> 8;
            if (r==0) {
                r = rand();
            }
        }
        *(subBuf+i) = r & 0xff;
        r = r >> 8;
    }
}

char * genstr_nonzero_impl(int len) {
    initRand();
    char * buf = nullptr;
    int cur = 0;
    if (len > 0) buf = (char*)malloc(len);
	if (buf == nullptr) return nullptr;

    while(len - cur> 0) {
        if (len - cur >= 3) {
            feed(buf+cur, 3);
            cur+=3;
        }else{
            feed(buf+cur, len - cur);
            cur+=len - cur;
        }

    }
    return buf;
}
/*
 * gen hex, every byte including 0-255
 */
char * genstr_impl(int len) {
    initRand();
    char * buf = nullptr;
    int cur = 0;
    if (len > 0) buf = (char*)malloc(len);
    if (buf == nullptr) return nullptr;
    int num;
    while(len - cur> 0) {
        num = rand();
        if (len - cur >= 3) {
            memcpy(buf+cur, &num, 3);
            cur+=3;
        }else{
            memcpy(buf+cur, &num, len - cur);
            cur+=len - cur;
        }

    }
    return buf;
}

/*
 * gen hex, every byte including 0-255
 */
std::string genstr_impl2(int len) {
    initRand();
    std::string buf;
    buf.reserve(len);
    int processed = 0;
    unsigned int num;
    while(processed < len) {
        num = rand();
        if (len - processed >= 3) {
            buf.push_back(num & 0xff);
            num >>= 8;
            buf.push_back(num & 0xff);
            num >>=8;
            buf.push_back(num &0xff);

            processed+=3;
        }else{
            auto left = len - processed;
            if (left == 1) {
                buf.push_back(num & 0xff);
            }else if (left ==2) {
                buf.push_back(num & 0xff);
                num >>= 8;
                buf.push_back(num & 0xff);
            }
            processed+=left;
        }

    }
    return buf;
}


