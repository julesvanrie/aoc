use std::env;
use std::fs;
use std::error::Error;
use std::collections::HashMap;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input();
    solve(&input, false);
    solve(&input, true);
    Ok(())
}

fn read_input() -> Vec<String> {
    let args: Vec<String> = env::args().collect();
    let file_name = format!("{}.txt", &args[1]);
    fs::read_to_string(file_name)
        .unwrap()
        .lines()
        .map(String::from)
        .collect()
}

fn solve(input: &Vec<String>, multi: bool) {
    let h = input.len();
    let w = input[0].len();

    let mut antennas: HashMap<char, Vec<(i16, i16)>> = HashMap::new();
    let mut antinodes: Vec<Vec<bool>> = vec![vec![false; w]; h];

    for (y, line) in input.into_iter().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c != '.' && c!= '#' {
                antennas.entry(c)
                        .and_modify(|a| a.push((y as i16, x as i16)))
                        .or_insert(vec![(y as i16, x as i16)]);
            }
        }
    }

    for antenna in antennas.values() {
        for (y_l, x_l) in antenna {
            for (y_r, x_r) in antenna {
                if (y_l, x_l) == (y_r, x_r) {
                    continue
                };
                let range = match multi {
                    true => 0..std::cmp::max(h as i16, w as i16),
                    false => 2..3
                };
                for i in range {
                    let y_a = y_l - i * (y_l - y_r);
                    let x_a = x_l - i * (x_l - x_r);
                    if y_a < h as i16 && x_a < w as i16 && y_a >= 0 && x_a >= 0 {
                        antinodes[y_a as usize][x_a as usize] = true;
                    }
                }
            }
        }
    }

    let result: usize = antinodes.into_iter().map(
        |row| row.into_iter().filter(|a| *a).count()
    ).sum();

    match multi {
        false =>  println!("The answer for part 1 is: {}", result),
        true => println!("The answer for part 2 is: {}", result)
    }
}
