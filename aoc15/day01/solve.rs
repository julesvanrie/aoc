use std::env;
use std::fs;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input()?;

    part_one(&input);
    part_two(&input);

    Ok(())
}

fn read_input() -> Result<String, Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();
    let file_name = format!("{}.txt", &args[1]);
    let file_content = fs::read_to_string(file_name)?;
    Ok(file_content.trim().to_string())
}

fn part_one(input: &str) {
    let answer_one = input.len() as i32
                   - 2 * input.matches(')').count() as i32;

    println!("The answer for part 1 is: {}", answer_one);
}

fn part_two(input: &str) {
    let mut floor = 0;
    let mut count = 0;
    let mut basement_entry = 0;

    for c in input.bytes() {
        // if c == b'(' {
        //     floor += 1
        // } else {
        //     floor -= 1
        // }
        floor += ((c == b'(') as i32) * 2 - 1;
        count += 1;
        if basement_entry == 0 && floor == -1 {
            basement_entry = count
        }
    }

    println!("The answer for part 1 is: {}", floor);
    println!("The answer for part 2 is: {}", basement_entry);
}
