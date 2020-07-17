
        # print("CURRENT ROOM: ", player.current_room.id)
        if player.current_room.id not in visited:
            visited[player.current_room.id] = dict()

            for room in player.current_room.get_exits():
                visited[player.current_room.id][room] = "?" 

        # Prioritize going to unknown values
        if "?" in list(visited[player.current_room.id].values()):
            rand = [None, None]
            while rand[1] != "?":
                rand = list(random.choices(list(visited[player.current_room.id].items()))[0]) # ['n', '?']
            traversal_path.append(rand[0])
            visited[player.current_room.id][rand[0]] = player.current_room.get_room_in_direction(rand[0]).id  
            old = player.current_room.id
            player.travel(rand[0])
        else:
            rand = list(random.choices(list(visited[player.current_room.id].items()))[0]) # ['n', '?']
            traversal_path.append(rand[0])
            player.travel(rand[0])

        # Add node we just travelled to
        if player.current_room.id not in visited:
            visited[player.current_room.id] = dict()
            for room in player.current_room.get_exits():
                visited[player.current_room.id][room] = "?" 

        # Edge-cases so we don't go back again while prioriting ?'s
        if rand[0] == "n":
            visited[player.current_room.id]["s"] = old
        elif rand[0] == "s":
            visited[player.current_room.id]["n"] = old
        elif rand[0] == "w":
            visited[player.current_room.id]["e"] = old
        elif rand[0] == "e":
            visited[player.current_room.id]["w"] = old