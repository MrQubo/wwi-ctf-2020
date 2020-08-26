use std::iter::FromIterator;
use std::fs;
use std::fs::File;
use std::io::Write;
use bytes::{Bytes, Buf, buf::BufExt};

#[derive(Debug)]
struct R {
    size: u32,
    reg: u32,
    taps: u32,
    invert: u32
}

fn getreg(seed: u32) -> u32 {
    ((seed << 1) & (!15)) | 8 | (seed & 7)
}

fn make17(seed: u32) -> R {
    R {
        size: 17,
        reg: getreg(seed),
        taps: (1<<0) | (1<<14),
        invert: 0
    }
}

fn make25(seed: u32) -> R {
    R {
        size: 25,
        reg: getreg(seed),
        taps: (1<<0) | (1<<3) | (1<<4) | (1<<14),
        invert: 1
    }
}

impl R {
    fn clock(&mut self) -> u32 {
        let to_reduce = self.reg & self.taps;
        let mut result: u32 = 0;
        for i in 0..(self.size-1) {
            result ^= to_reduce >> i;
        }
        result &= 1;
        result ^= self.invert;
        self.reg = (self.reg >> 1) | (result << (self.size - 1));
        result
    }
    fn get_byte(&mut self) -> u8 {
        let mut ret: u32 = 0;
        for _ in 1..8 {
            ret = (ret << 1) | self.clock();
        }
        ret as u8
    }
}

fn encrypt_data(key17: u32, key25: u32, data: &Bytes) -> Bytes {
    let mut r17 = make17(key17);
    let mut r25 = make25(key25);
    Bytes::from_iter(data.iter().map(|&b| { 
        b ^ r17.get_byte() ^ r25.get_byte()
    }))
}

fn main() {
    let flag = Bytes::from(fs::read_to_string("flag.txt")
        .expect("Coś się nie udało"));
    let data = b"oto flaga, prosze czytac: "[..].chain(flag).to_bytes();
    let key17: u32 = rand::random::<u32>() & 0x001ffff;
    let key25: u32 = rand::random::<u32>() & 0x1ffffff;
    let encrypted = encrypt_data(key17, key25, &data);
    let mut enc = File::create("enc.bin").expect("nie udało się otworzyć");
    enc.write_all(encrypted.bytes()).expect("nie udało się zapisać");
    println!("{:?}", encrypted);
}
