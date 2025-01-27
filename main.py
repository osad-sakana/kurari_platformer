from game import Game


if __name__ == "__main__":
    # game = Game()
    # game.run()
    from map import Map
    map = Map()
    map.load_map("stage0.json")
    print(map.map_data)
