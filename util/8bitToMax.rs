use std::io::{self, Read, Write};

fn main() {
    let stdout = io::stdout();
    let stdin = io::stdin();
    let mut output = stdout.lock();

    let mut offset = 0;
    let mut buf = 0;

    for sim_data in stdin.lock().bytes() {
        offset = (offset + 3) % 4;

        let sim_data = sim_data.expect("I/O error reading input");

        // Get magnitude. It looks like the max value is 64.
        // Will use (0 <= val <= 31) for mag to be 0
        // and (val > 31) to be a mag of 1.
        // Our software will treat 0's as 1.0/3.0 and 1's as 1.0
        let mag_bit = if sim_data as i8 > 31 { 1 } else { 0 };

        // Get sign. Since 2s complement, most significant bit determines the
        // sign. A value of 1 means sign is negative (in both 2s complement, and
        // the two bit sign/mag max data).
        let sign_bit = sim_data >> 7;

        buf |= ((mag_bit << 1) | sign_bit) << (offset * 2);

        if offset == 0 {
            output.write_all(&[buf]).expect("I/O error writing output");
            buf = 0;
        }
    }
}
