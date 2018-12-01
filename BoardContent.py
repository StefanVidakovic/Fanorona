#Board state is represented as a graph for the purpose of the AI
#as it is much simpler to update and can contain more vital information
#such as edges. The multidimensional board_array was used for convenience
#in manipulating and updating the UI.
class BoardContent():

    '''Type to represent complete board state
        from coordinate tuple.

    Attributes:
        dictionary: ._board
    '''

    EMPTY = 0
    WHITE = 1
    BLACK = 2

    def __init__(self):
        self._board = dict()

    def add_vertex(self, v):
        ''' Adds a new vertex with identifier v to the graph.

        Args:
            v (hashable type): the vertex identifier to be added.

        Raises:
            RuntimeError: If the vertex was already in the graph.
        '''
        if v in self._board:
            raise RuntimeError("Bad argument:"
                               " Vertex {} already in the graph".format(v))
        self._board[v] = [None]

    def add_piece_token(self,v,pearl):
        '''Adds piece data to corresponding vertex.

        Args:
            v: vertex that is on the board
            pearl: EMPTY, WHITE, BLACK

        Raises:
            RuntimeError: If the vertex is not on the board.
        '''
        if v not in self._board.keys():
                raise RuntimeError("Bad argument:"
                                    "Vertex {} not in graph".format(v))
        self._board[v][0] = pearl

    def pearl_update(self,v,u):
        '''Changes the pearl information of specified vertex to
            that of old index and Sets old vertex pearl info to
            EMPTY. Corresponds to moving a piece from u to v.

            Args:
                v: new vertex that is on the board
                u: old vertex that is on the board

            Raises:
                RuntimeError: If either vertex is not on the board
        '''
        if v not in self._board.keys():
            raise RuntimeError("Bad argument:"
                                "Vertex {} not in graph".format(v))
        if u not in self._board.keys():
            raise RuntimeError("Bad argument:"
                                "Vertex {} not in graph".format(u))
        self.add_piece_token(v,self._board[u][0])
        self.add_piece_token(u,self.EMPTY)


    def add_edge(self, e):
        ''' Adds edge e to the graph.

        Args:
            e (tuple of two hashables): The edge to be added as a tuple. The
                edge goes from e[0] to e[1]

        Raises:
            RuntimeError: When one of the verticies is not a vertex.
        '''
        if e[0] not in self._board.keys():
            raise RuntimeError("Attempt to create an edge with"
                               "non-existent vertex: {}".format(e[0]))
        if e[1] not in self._board.keys():
            raise RuntimeError("Attempt to create an edge with"
                               "non-existent vertex: {}".format(e[1]))

        self._board[e[0]].append(e[1])
        self._board[e[1]].append(e[0])

    def neighbours(self, v):
        '''Returns the list of vertices that are neighbours to v.'''
        return self._board[v][1:]

    def make_board_graph(self,board_array,height,width):
        ''' Makes an instance of the graph class to represent
             the inputted board_array.
        Args:
            board_array (multidimensional array): The board to be made.
            height: integer representing the board height.
            width: integer representing the board width.
        '''
        for j in range(width):
            for i in range(height):
                self.add_vertex((i,j))
                self.add_piece_token((i,j),board_array[i][j])

        for i in range(height-1):
            for j in range(width):
                if i%2==0:
                    if j==0:
                        self.add_edge(((i,0),(i+1,1)))
                    if j==2:
                        self.add_edge(((i,2),(i+1,1)))
                        self.add_edge(((i,2),(i+1,3)))
                    if j==4:
                        self.add_edge(((i,4),(i+1,3)))
                if not i%2==0:
                    if not j%2==0:
                        self.add_edge(((i,j),(i+1,j-1)))
                        self.add_edge(((i,j),(i+1,j+1)))
        for i in range(height):
            for j in range(width-1):
                self.add_edge(((i,j),(i,j+1)))
        for j in range(width):
            for i in range(height-1):
                self.add_edge(((i,j),(i+1,j)))

    def open_neighbours(self,v):
        ''' Returns the vertices that are connected to v
             and that contain no pearls.
        Args:
            vertex: a vertex in the board graph.
        '''
        return [o for o in self.neighbours(v) if self._board[o][0]==self.EMPTY]

    def within_board(self,v):
        '''Checks whether a vertex v is in the boardgraph.
        '''
        if v in self._board.keys():
            return True
        else:
             return False
    def remake_board_array(self,width,height):
        '''Translates board graph representation back to
            multidimensional array representation for UI purposes.
        Args:
            width: width of board.
            height: height of board.
        '''
        board_array = [[BoardContent.EMPTY for i in range(width)] for j in range(height)]
        for v in self._board.keys():
            board_array[v[0]][v[1]] = self._board[v][0]
        return board_array
