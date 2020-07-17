import random
import time

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.reset()

    def reset(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            return False
            # print("WARNING: You cannot be friends with yourself")
            return False
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            # print("WARNING: Friendship already exists")
            pass
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
        return True  # Success!

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.reset()
        # !!!! IMPLEMENT ME

        # Add users
        for i in range(num_users):
            self.add_user(f"User {i}")

        # Create friendships
        possible_friendships = list()

        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

        # Shuffle the possible friendships
        random.shuffle(possible_friendships)

        # Add friendships
        for i in range(num_users * avg_friendships // 2):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])


    def populate_graph_2(self, num_users, avg_friendships):
        # Reset graph
        self.reset()
        collisions = 0
       
        # Add users
        for i in range(num_users):
            self.add_user(f"User {i}")

        # Create friendships
        target_friendships = num_users * avg_friendships
        total_friendships = 0

        while total_friendships < target_friendships:
            user_id = random.randint(1, self.last_id)
            friend_id = random.randint(1, self.last_id)

            if self.add_friendship(user_id, friend_id):
                total_friendships += 2
            else:
                collisions += 1

        print(f"COLLISIONS: {collisions}")

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = dict()  # Note that this is a dictionary, not a set
        arrayList = list()

        q = Queue()
        q.enqueue([user_id])

        while q.size() > 0:
            path = q.dequeue()
            arrayList.append(path)

            v = path[-1]

            if v not in visited:
                # Add it to visited, as key, and its history as values
                # arrayList[-1] should be the history for V
                visited[v] = arrayList[-1]

                # Now we just need to setup get_paths(v) to traverse all other verts in BFT
                for next_vert in self.friendships[v]:
                    newPath = list(path)
                    newPath.append(next_vert)
                    q.enqueue(newPath)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()

    start_time = time.time()
    sg.populate_graph(300, 150)
    end_time = time.time()
    print(f"O(n^2) runtime: {end_time - start_time}")
    # print(sg.friendships)
    start_time = time.time()
    sg.populate_graph_2(300, 150)
    end_time = time.time()
    print(f"O(n) runtime: {end_time - start_time}")
    # connections = sg.get_all_social_paths(1)
    # print(connections)


"""

QUESTIONS:
To create 100 users with an average of 10 friends each, how many times would you need to call add_friendship()? Why? 

# (100 * 10 // 2):  500. Since we choose a random person to befriend, we could choose ourselves, or people we're friends with already so this on an estimate, would give  us the average amount of friends we want per person.

If you create 1000 users with an average of 5 random friends each, what percentage of other users will be in a particular user's extended social network? What is the average degree of separation between a user and those in his/her extended network? 

# Assuming this means what's the average length of each array for the problem I just solved, I'm gonna say 5. 

"""

"""

STRETCH: 
You might have found the results from question #2 above to be surprising. Would you expect results like this in real life? If not, what are some ways you could improve your friendship distribution model for more realistic results?

# I would expect results like this in real life. Because when there's groups of friends, one friend from each clique tends to know eachother, connecting both groups from a graph perspective. One way I would upgrade this algorithm is by having what I just said as an edge-case (where both groups don't have friends from each other, so make the recommendation. Maybe through GPS location. If they're close enough area wise, suggest the most popular person from the group (based on follower's))

"""