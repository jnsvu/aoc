use itertools::Itertools;
use std::collections::HashMap;

#[derive(Debug)]
struct Blueprint {
    id: usize,
    costs: [[usize; 3]; 4],
}

type Materials = (usize, usize, usize, usize);

type Robots = Vec<usize>;

const MINUTES: i32 = 24;

fn get_blueprints() -> Vec<Blueprint> {
    let blueprints: Vec<_> = include_str!("./data.txt")
        .split("\n")
        .enumerate()
        .map(|(i, bp)| {
            let lines: Vec<_> = bp
                .split(".")
                .map(|l| l.split("robot costs ").last().unwrap())
                .collect();

            Blueprint {
                id: i + 1,
                costs: [
                    [
                        lines[0].rsplit_once(" ore").unwrap().0.parse().unwrap(),
                        0,
                        0,
                    ],
                    [
                        lines[1].rsplit_once(" ore").unwrap().0.parse().unwrap(),
                        0,
                        0,
                    ],
                    [
                        lines[2].rsplit_once(" ore").unwrap().0.parse().unwrap(),
                        lines[2].split(" ").nth(3).unwrap().parse().unwrap(),
                        0,
                    ],
                    [
                        lines[3].rsplit_once(" ore").unwrap().0.parse().unwrap(),
                        0,
                        lines[3].split(" ").nth(3).unwrap().parse().unwrap(),
                    ],
                ],
            }
        })
        .collect();

    return blueprints;
}

fn can_buy(cost: [usize; 3], materials: Materials) -> bool {
    let (ores, clay, obsidian, _) = materials;
    return cost[0] <= ores && cost[1] <= clay && cost[2] <= obsidian;
}

fn should_buy(i: usize, robots: &Robots, max_robots: &Robots) -> bool {
    return robots[i] < max_robots[i];
}

fn solve(
    bp: &Blueprint,
    minutes: i32,
    materials: Materials,
    robots: Robots,
    max_robots: &Robots,
    current_max: usize,
    cache: &mut HashMap<(Materials, Robots), i32>,
) -> usize {
    let (ores, clay, obsidian, geode) = materials;

    if minutes < 1 {
        return current_max;
    }

    let mut max = current_max;

    bp.costs.iter().enumerate().rev().for_each(|(i, &cost)| {
        if can_buy(cost, materials) && should_buy(i, &robots, max_robots) {
            let next_materials = (
                ores + robots[0] - cost[0],
                clay + robots[1] - cost[1],
                obsidian + robots[2] - cost[2],
                geode + robots[3],
            );

            let next_robots = vec![
                robots[0] + if i == 0 { 1 } else { 0 },
                robots[1] + if i == 1 { 1 } else { 0 },
                robots[2] + if i == 2 { 1 } else { 0 },
                robots[3] + if i == 3 { 1 } else { 0 },
            ];

            let cached_max = *cache
                .get(&(next_materials, next_robots.to_vec()))
                .unwrap_or(&0);

            if cached_max < minutes {
                cache.insert((next_materials, next_robots.to_vec()), minutes);

                max = solve(
                    bp,
                    minutes - 1,
                    next_materials,
                    next_robots,
                    max_robots,
                    current_max + robots[3],
                    cache,
                )
                .max(max);
            }
        }
    });

    max = solve(
        bp,
        minutes - 1,
        (
            ores + robots[0],
            clay + robots[1],
            obsidian + robots[2],
            geode + robots[3],
        ),
        robots.to_vec(),
        max_robots,
        current_max + robots[3],
        cache,
    )
    .max(max);

    return max;
}

fn p1() {
    let blueprints = get_blueprints();
    let quality_levels: Vec<_> = blueprints
        .iter()
        .map(|bp| {
            let max_robots = (0..3)
                .map(|ore_i| bp.costs.iter().fold(0, |a, costs| a.max(costs[ore_i])))
                .chain([i32::MAX as usize])
                .collect_vec();

            let max_geocides = solve(
                bp,
                MINUTES,
                (0, 0, 0, 0),
                vec![1, 0, 0, 0],
                &max_robots,
                0,
                &mut HashMap::new(),
            );
            println!("max {:?}", max_geocides);
            return max_geocides;
        })
        .collect();

    print!("{}", quality_levels.iter().sum::<usize>())
}

fn p2() {
    let binding = get_blueprints();
    let blueprints: Vec<_> = binding.iter().take(3).collect();

    let max_geodes: Vec<_> = blueprints
        .iter()
        .map(|bp| {
            let max_robots = (0..3)
                .map(|ore_i| bp.costs.iter().fold(0, |a, costs| a.max(costs[ore_i])))
                .chain([i32::MAX as usize])
                .collect_vec();

            return solve(
                bp,
                32,
                (0, 0, 0, 0),
                vec![1, 0, 0, 0],
                &max_robots,
                0,
                &mut HashMap::new(),
            );
        })
        .collect();

    print!("{}", max_geodes.iter().product::<usize>())
}

fn main() {
    p1();
    p2();
}
