    import sys
    import random


    # Map data structure declaration
    class Map:
        def __init__(self, _nzone, _nlink, _podamount):
            self.nzone = _nzone
            self.nlink = _nlink
            self.pod_amount = _podamount

            self.bases = [0 for _ in range(self.pod_amount)]
            self.plats = [0 for _ in range(self.nzone)]
            self.visibs = [0 for _ in range(self.nzone)]
            self.owners = [-1 for _ in range(self.nzone)]
            self.distances = [-1 for _ in range(self.nzone)]
            self.links = [[] for _ in range(self.nzone)]
            self.pods = [[0 for _ in range(self.pod_amount)] for _ in range(self.nzone)]

        def init_distance(self, _zone, _distances, _distance):
            _distances[_zone] = _distance
            print(_zone, _distance, file=sys.stderr)

            counted = []
            for i in range(len(self.links[_zone])):
                target_value = _distances[self.links[_zone][i]]
                if (target_value > _distances[_zone] or target_value == -1) and _distance < 25:
                    counted.append(i)
                    _distances[self.links[_zone][i]] = _distance + 1

            print(counted, file=sys.stderr)

            for i in range(len(counted)):
                if i == len(counted) // 2:
                    self.init_distance(self.links[_zone][counted[i]], _distances, _distance + 1)

        def assign_base(self):
            for i in range(len(self.visibs)):
                if self.visibs[i] == 1 and self.owners[i] != -1:
                    self.bases[self.owners[i]] = i

        def dead_end(self, zone):
            for i in range(len(self.links[zone])):
                if self.distances[self.links[zone][i]] == -1:
                    return False
                elif self.distances[zone] < self.distances[self.links[zone][i]]:
                    return False
            return True

        def prints(self):
            print(self.links, file=sys.stderr)

        def add_link(self, _zone1, _zone2):
            self.links[_zone1].append(_zone2)
            self.links[_zone2].append(_zone1)

        def update_platinum(self, _zone, _plat):
            self.plats[_zone] = _plat

        def update_owner(self, _zone, _owner):
            self.owners[_zone] = _owner

        def update_pods(self, _zone, _owner, _pods):
            self.pods[_zone][_owner] = _pods

        def update_visibs(self, _zone, _visib):
            self.visibs[_zone] = _visib

        def visible(self, _zone):
            return self.visibs[_zone]

        def owner(self, _zone):
            return self.owners[_zone]

        def plat(self, _zone):
            return self.plats[_zone]

        def get_pod(self, _zone, _owner):
            return self.pods[_zone][_owner]

        def get_enemy_pods(self, _zone, _id):
            count = 0
            for i in range(len(self.pods[_zone])):
                if i != _id:
                    count += self.pods[_zone][i]
            return count

        def enemy_base(self, zone, me):
            for i in range(len(self.bases)):
                if zone == self.bases[i] and i != me:
                    return True
            return False


    # Function of determine the direction of movement of the pod
    def move_decision(zone, map, moves, me, turn):
        pod_amount_map = map.get_pod(zone, me)
        dec_val = []

        if map.get_enemy_pods(zone, me) > 0:
            return None;
        # If the plot is safe, weigh the position around
        for i in range(len(map.links[zone])):
            if map.get_enemy_pods(map.links[zone][i], me) > 0 or map.enemy_base(map.links[zone][i],
                                                                                me):  # Chase the enemy
                dec_val.append(30)
            elif map.owner(map.links[zone][i]) == me:  # Avoid passing through the plots that have been mastered
                dec_val.append(-6)
            else:  # Take over the enemy plots
                dec_val.append(map.plat(map.links[zone][i]))
                if map.owner(map.links[zone][i]) != me and map.owner(map.links[zone][i]) != -1:
                    dec_val[i] += 4

        if turn < 10:
            move_amount = (pod_amount_map // 2) + 1
        else:
            move_amount = ((pod_amount_map * 3) // 4) + 1

        moves.append([move_amount, zone, get_max(dec_val, map, zone)])
        if map.distances[get_max(dec_val, map, zone)] == -1 or map.distances[get_max(dec_val, map, zone)] > \
                map.distances[zone]:
            map.distances[get_max(dec_val, map, zone)] = map.distances[zone] + 1
            if map.dead_end(get_max(dec_val, map, zone)):
                map.distances[get_max(dec_val, map, zone)] -= 1


    def get_max(dec_val, map, zone):
        max_val = max(dec_val)
        max_dex = dec_val.index(max_val)

        if max_val == -6:
            distance = []
            for i in range(len(map.links[zone])):
                distance.append(map.distances[map.links[zone][i]])

            max_val = max(distance)
            duplicate = []
            # Checks 2 points with the same priority level
            for i in range(len(distance)):
                if max_val == distance[i]:
                    duplicate.append(i)
            if len(duplicate) > 1:
                max_dex = duplicate[random.randint(0, len(duplicate) - 1)]
            else:
                max_dex = distance.index(max_val)
        return map.links[zone][max_dex]


    player_count, my_id, zone_count, link_count = [int(i) for i in input().split()]
    map = Map(zone_count, link_count, player_count)

    # Map value initialization
    for i in range(zone_count):
        zone_id, platinum_source = [int(j) for j in input().split()]
        map.update_platinum(zone_id, platinum_source)

    for i in range(link_count):
        zone_1, zone_2 = [int(j) for j in input().split()]
        map.add_link(zone_1, zone_2)

    turn = 0
    while True:
        my_platinum = int(input())  # your available Platinum

        for i in range(zone_count):
            # z_id: this zone's ID
            # owner_id: the player who owns this zone (-1 otherwise)
            # pods_p0: player 0's PODs on this zone
            # pods_p1: player 1's PODs on this zone
            # visible: 1 if one of your units can see this tile, else 0
            # platinum: the amount of Platinum this zone can provide (0 if hidden by fog)
            z_id, owner_id, pods_p0, pods_p1, visible, platinum = [int(j) for j in input().split()]
            map.update_owner(z_id, owner_id)
            map.update_pods(z_id, 0, pods_p0)
            map.update_pods(z_id, 1, pods_p1)
            map.update_visibs(z_id, visible)
            map.update_platinum(z_id, platinum)

        if turn == 0:
            print(map.visibs, file=sys.stderr)
            map.assign_base()
            print(map.bases, file=sys.stderr)
            map.distances[map.bases[my_id]] = 0

        move = []
        # Iteration through all the zones on the map to find a friendly pod and apply move_decision
        for zone in range(zone_count):
            myPod = map.get_pod(zone, my_id)
            if myPod > 0:
                move_decision(zone, map, move, my_id, turn)

        for i in range(len(move)):
            print(move[i][0], move[i][1], move[i][2], end=" ")

        print("")
        print("WAIT")
        turn += 1