use std::env;
use std::fs;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input();
    solve_one(&input);
    solve_two(&input);
    Ok(())
}

fn read_input() -> Vec<usize> {
    let args: Vec<String> = env::args().collect();
    let file_name = format!("{}.txt", &args[1]);
    fs::read_to_string(file_name)
        .unwrap()
        .trim()
        .chars()
        .map(|c| c.to_digit(10).unwrap() as usize)
        .collect()
}

fn solve_one(blocks: &Vec<usize>) {
    let mut result = 0;

    let mut position = 0;
    let mut fill_id = (blocks.len() - 1) / 2;
    let mut fill_left = blocks[fill_id * 2];

    for id in 0..(blocks.len() / 2) {
        // Count the blocks that are left for the case of the last file we will only move partly
        let mut blocks_left = blocks[id * 2];
        if id == fill_id { blocks_left = fill_left }
        // We encounter a file, so we calculate the checksum
        for block in 0..blocks_left {
            result += (position + block) * id
        }
        // If we are done
        if id >= fill_id { break }
        position += blocks[id * 2];
        // We encounter some free space, so move the last block in here
        for block in 0..blocks[id * 2 + 1] {
            if fill_left == 0 {
                fill_id -= 1;
                fill_left = blocks[fill_id * 2];
                if fill_id <= id { break }
            }
            // And calculate the checksum
            result += (position + block) * fill_id;
            fill_left -= 1;
        }
        position += blocks[id * 2 + 1];
    }

    println!("The answer for part 1 is: {}", result);
}

fn solve_two(blocks: &Vec<usize>) {
    let mut result = 0;
    let nb_files = blocks.len() / 2 + 1;
    let files = blocks.iter().step_by(2);

    // First, we need to calculate the position of each block
    let mut positions = vec![0; nb_files];
    for id in 0..nb_files {
        positions[id] = blocks[0..id*2].iter().sum();
    }

    // Then, we need to calculate the empty spaces' position and size
    let mut empties = vec![(0, 0); nb_files - 1];
    for ix in 0..(nb_files - 1) {
        empties[ix] = (blocks[0..ix*2+1].iter().sum(), blocks[ix*2+1]);
    }

    // Now, we can start moving the blocks one by one, starting from the end
    for (id, size) in (0..nb_files).rev().zip(files.rev()) {
        // println!("{:?}", (id, size));
        // Check the empty spaces one by one
        let mut used_empty_ix: Option<usize> = None;
        for (ix, (empty_pos, empty_size)) in empties.iter().enumerate() {
            if empty_size >= size && empty_pos < &positions[id] {
                positions[id] = *empty_pos;
                used_empty_ix = Some(ix);
            }
        }
        // Update the empty blocks
        match used_empty_ix {
            Some(ix) => {
                if empties[ix].1 == *size {
                    empties.remove(ix);
                } else {
                    empties[ix] = (empties[ix].0 + size, empties[ix].1 - size);
                }
            },
            None => ()
        }
    }

    // Finally, calculate the checksum
    for (id, pos) in positions.iter().enumerate() {
        for i in 0..blocks[id*2] {
            result += (pos + i) * id;
        }
    }

    println!("The answer for part 1 is: {}", result);
}
