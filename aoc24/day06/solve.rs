use std::env;
use std::fs;
use std::error::Error;
use std::collections::{HashMap, HashSet};

fn main() -> Result<(), Box<dyn Error>> {
    let mut solution = Solution::new();
    solution.solve_one();
    solution.solve_two();
    Ok(())
}

struct Visit {
    x: usize,
    y: usize,
    direction: u8
}

struct Solution {
    grid: Vec<Vec<char>>,
    visited: HashSet<(usize, usize)>,
    start: Visit
}

impl Solution {
    fn new() -> Solution {
        let input = Solution::read_input();
        let grid: Vec<Vec<char>> = input.lines()
                    .map(|line| line.chars().collect())
                    .collect();
        let start = Solution::get_start(&grid);

        Solution {
            grid: grid,
            visited: HashSet::new(),
            start: start
        }
    }

    fn read_input() -> String {
        let args: Vec<String> = env::args().collect();
        let file_name = format!("{}.txt", &args[1]);
        fs::read_to_string(file_name)
            .unwrap()
    }

    fn get_start(grid: &Vec<Vec<char>>) -> Visit {
        let mut start: (usize, usize, u8) = (0, 0, 5);
        for y in 0..grid.len() {
            for x in 0..grid[0].len() {
                let dir = grid[y][x];
                start.2 = match dir {
                    '^' => 0,
                    '>' => 1,
                    'v' => 2,
                    '<' => 3,
                    _ => 5

                };
                start.0 = y;
                start.1 = x;
                if start.2 < 5 {
                    break
                }
            }
            if start.2 < 5 {
                break
            }
        }
        Visit {y: start.0, x: start.1, direction: start.2}
    }

    fn solve_one(&mut self) {
        let (mut y, mut x, mut direction) = (self.start.y, self.start.x, self.start.direction);

        loop {
            let mut go_further = || -> Result<(), &str> {
                let (new_y, new_x) = self.next_pos(y, x, direction)?;
                if *self.grid.get(new_y).ok_or("OoB")?.get(new_x).ok_or("OoB")? != '#' {
                    y = new_y;
                    x = new_x;
                } else {
                    direction = (direction + 1) % 4;
                }
                Ok(())
            };

            if let Err(_err) = go_further() {
                break
            }

            self.visited.insert((y, x));
        }

        println!("The answer for part 1 is: {}", self.visited.len());
    }

    fn solve_two(&mut self) {
        let mut result: i32 = 0;

        for (obstacle_y, obstacle_x) in &self.visited {
            self.grid[*obstacle_y][*obstacle_x] = '#';
            let mut visited: HashMap<(usize, usize), Vec<u8>> = HashMap::new();
            let mut y = self.start.y;
            let mut x = self.start.x;
            let mut direction = self.start.direction;

            loop {
                let mut go_further = || -> Result<(), &str> {
                    let (new_y, new_x) = self.next_pos(y, x, direction)?;
                    if *self.grid.get(new_y).ok_or("OoB")?.get(new_x).ok_or("OoB")? != '#' {
                        visited.entry((y,x)).or_insert(vec![direction]).push(direction);
                        y = new_y;
                        x = new_x;
                    } else {
                        direction = (direction + 1) % 4;
                    }
                    Ok(())
                };

                if let Err(_err) = go_further() {
                    self.grid[*obstacle_y][*obstacle_x] = '.';
                    break
                }

                if visited.get(&(y,x)).map_or(false, |vis| vis.contains(&direction)) {
                    result += 1;
                    self.grid[*obstacle_y][*obstacle_x] = '.';
                    break
                }

            }
        }

        println!("The answer for part 2 is: {}", result);
    }

    fn next_pos(&self, y: usize, x: usize, direction: u8) -> Result<(usize, usize), &str> {
        match direction {
            0 => y.checked_sub(1).map(|new_y| (new_y, x)).ok_or("Underflow on y-1"),
            1 => x.checked_add(1).map(|new_x| (y, new_x)).ok_or("Overflow on x+1"),
            2 => y.checked_add(1).map(|new_y| (new_y, x)).ok_or("Overflow on y+1"),
            3 => x.checked_sub(1).map(|new_x| (y, new_x)).ok_or("Underflow on x-1"),
            _ => Err("Invalid direction"),
        }
    }
}
