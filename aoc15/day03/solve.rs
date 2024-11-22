use std::env;
use std::fs;
use std::error::Error;
use std::collections::HashMap;

#[derive(Hash, Eq, PartialEq, Debug)]
struct Coord { x: i32, y: i32 }
impl Coord {
    fn new(x: i32, y: i32) -> Coord {
        Coord { x: x, y: y }
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input()?;

    println!("The answer for part 1 is: {}", solve(&input, 1));
    println!("The answer for part 2 is: {}", solve(&input, 2));

    Ok(())
}

fn read_input() -> Result<String, Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();
    let file_name = format!("{}.txt", &args[1]);
    let file_content = fs::read_to_string(file_name)?;
    Ok(file_content.trim().to_string())
}

fn solve(input: &str, part: i32) -> usize {
    let mut presents: HashMap<Coord, i32> = HashMap::new();

    let mut x1 = 0; let mut x2 = 0;
    let mut y1 = 0; let mut y2 = 0;

    // Keep track if it's Santa (1) or Robo-Santa (2)
    let mut turn = 1;

    // Base position start with a present
    presents.insert(Coord::new(0, 0), 1);

    for c in input.bytes() {
        let x: &mut i32;
        let y: &mut i32;

        // Switch turns if part two
        if turn == 1 {
            x = &mut x1;
            y = &mut y1;
            turn = part; // Stay with 1 if part one
        } else {
            x = &mut x2;
            y = &mut y2;
            turn = 1;
        }

        match c {
            b'>' => *x += 1,
            b'<' => *x -= 1,
            b'^' => *y += 1,
            b'v' => *y -= 1,
            _ =>  ()
        }
        presents.entry(Coord::new(*x, *y))
            .and_modify(|count| *count += 1)
            .or_insert(1);

    }

    presents.len()
}
