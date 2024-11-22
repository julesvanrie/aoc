use std::env;
use std::fs;
use std::error::Error;
use std::str::FromStr;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input();

    solve(&input);

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

fn solve(input: &Vec<String>) {
    let mut total_paper = 0;
    let mut total_ribbon = 0;

    for line in input {
        let dims: Vec<i32> = line.split('x')
                            .filter_map(|x| i32::from_str(x).ok())
                            .collect();
        let (l, w, h) = (dims[0], dims[1], dims[2]);

        let surfaces = [l*w, l*h, w*h];
        let paper = 2 * surfaces.iter().sum::<i32>()
                    + surfaces.iter().min().unwrap();
        total_paper += paper;

        let sides = [l+w, l+h, w+h];
        let ribbon = 2 * sides.iter().min().unwrap()
                     + l*w*h;
        total_ribbon += ribbon;
    }

    println!("The answer for part 1 is: {}", total_paper);
    println!("The answer for part 2 is: {}", total_ribbon);
}
