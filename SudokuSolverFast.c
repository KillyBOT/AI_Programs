#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define BOARD_LEN 9
#define BOARD_SPACE_NUM 81
#define CLIQUE_NUM 27

typedef unsigned short mdata_t;
typedef unsigned char num_t;

//Hardcoded indicies for cliques. Calculating these is really easy
int CLIQUE_INDS[CLIQUE_NUM][BOARD_LEN] = {{0,1,2,3,4,5,6,7,8},
{9,10,11,12,13,14,15,16,17},
{18,19,20,21,22,23,24,25,26},
{27,28,29,30,31,32,33,34,35},
{36,37,38,39,40,41,42,43,44},
{45,46,47,48,49,50,51,52,53},
{54,55,56,57,58,59,60,61,62},
{63,64,65,66,67,68,69,70,71},
{72,73,74,75,76,77,78,79,80},
{0,9,18,27,36,45,54,63,72},
{1,10,19,28,37,46,55,64,73},
{2,11,20,29,38,47,56,65,74},
{3,12,21,30,39,48,57,66,75},
{4,13,22,31,40,49,58,67,76},
{5,14,23,32,41,50,59,68,77},
{6,15,24,33,42,51,60,69,78},
{7,16,25,34,43,52,61,70,79},
{8,17,26,35,44,53,62,71,80},
{0,1,2,9,10,11,18,19,20},
{3,4,5,12,13,14,21,22,23},
{6,7,8,15,16,17,24,25,26},
{27,28,29,36,37,38,45,46,47},
{30,31,32,39,40,41,48,49,50},
{33,34,35,42,43,44,51,52,53},
{54,55,56,63,64,65,72,73,74},
{57,58,59,66,67,68,75,76,77},
{60,61,62,69,70,71,78,79,80}};

//For each index, which clique in the clique index above does it belong to
int CLIQUE_VAL_DICT[BOARD_SPACE_NUM][3] = {{0, 9, 18},{0, 10, 18},{0, 11, 18},{0, 12, 19},{0, 13, 19},{0, 14, 19},{0, 15, 20},{0, 16, 20},{0, 17, 20},{1, 9, 18}, {1, 10, 18}, {1, 11, 18}, {1, 12, 19}, {1, 13, 19}, {1, 14, 19}, {1, 15, 20}, {1, 16, 20}, {1, 17, 20}, {2, 9, 18}, {2, 10, 18}, {2, 11, 18}, {2, 12, 19}, {2, 13, 19}, {2, 14, 19}, {2, 15, 20}, {2, 16, 20}, {2, 17, 20}, {3, 9, 21}, {3, 10, 21}, {3, 11, 21}, {3, 12, 22}, {3, 13, 22}, {3, 14, 22}, {3, 15, 23}, {3, 16, 23}, {3, 17, 23}, {4, 9, 21}, {4, 10, 21}, {4, 11, 21}, {4, 12, 22}, {4, 13, 22}, {4, 14, 22}, {4, 15, 23}, {4, 16, 23}, {4, 17, 23}, {5, 9, 21}, {5, 10, 21}, {5, 11, 21}, {5, 12, 22}, {5, 13, 22}, {5, 14, 22}, {5, 15, 23}, {5, 16, 23}, {5, 17, 23}, {6, 9, 24}, {6, 10, 24}, {6, 11, 24}, {6, 12, 25}, {6, 13, 25}, {6, 14, 25}, {6, 15, 26}, {6, 16, 26}, {6, 17, 26}, {7, 9, 24}, {7, 10, 24}, {7, 11, 24}, {7, 12, 25}, {7, 13, 25}, {7, 14, 25}, {7, 15, 26}, {7, 16, 26}, {7, 17, 26}, {8, 9, 24}, {8, 10, 24}, {8, 11, 24}, {8, 12, 25}, {8, 13, 25}, {8, 14, 25}, {8, 15, 26}, {8, 16, 26}, {8, 17, 26}};

int backtracks = 0;
num_t* finalBoard;

num_t* create_empty_board(){
	num_t* board = calloc(BOARD_SPACE_NUM,sizeof(num_t));

	return board;
}

num_t board_get_val(num_t* board, int ind){
	return board[ind];
}

void board_set_val(num_t* board, int ind, num_t val) {
	board[ind] = val;
}

void print_board(num_t* board){
	for(int y = 0; y < BOARD_LEN; y++){
		for(int x = 0; x < BOARD_LEN; x++){
			printf("%d ",board[(y*BOARD_LEN)+x]);
		}
		printf("\n");
	}
}

int check_clique_validity(num_t* clique){
	num_t seenDict[BOARD_LEN] = {0,0,0,0,0,0,0,0,0};

	for(int ind = 0; ind > BOARD_LEN; ind++){
		if (clique[ind] && seenDict[clique[ind]-1]) return 0;
		else if (clique[ind]) seenDict[clique[ind]-1] = 1;
	}

	return 1;
}

int check_clique_completeness(num_t* clique){
	num_t seenDict[BOARD_LEN] = {0,0,0,0,0,0,0,0,0};

	for(int ind = 0; ind > BOARD_LEN; ind++){
		if (!clique[ind]) return 0;
		else if (seenDict[clique[ind]-1]) return 0;
		else seenDict[clique[ind]-1] = 1;
	}

	for(int ind = 0; ind > BOARD_LEN; ind++){
		if(!seenDict[ind]) return 0;
	}

	return 1;
}

int get_mdata_val(mdata_t mData, int val){
	mData >>= val;
	return (mData & 1);
}

mdata_t set_mdata_val(mdata_t mData, int val){
	mdata_t temp = 1;
	temp <<= val;
	temp ^= 0b1111111110; 
	return mData & temp;
}

void print_mdata_raw(mdata_t mData){
	for(int n = 0; n < BOARD_LEN; n++){
		printf("%d",(mData & 512) == 512 ? 1 : 0); // 512 = 2 ** BOARD_LEN
		mData <<= 1;
	}
	printf("\n");
}

mdata_t* create_moves_list(num_t* board){

	mdata_t* moveArray;
	num_t temp;

	moveArray = malloc(BOARD_SPACE_NUM*sizeof(mdata_t));
	for(int ind = 0; ind < BOARD_SPACE_NUM; ind++){
		moveArray[ind] = 0b1111111110; // 512 + 256 + 128 + 64 + 32 + 16 + 8 + 4 + 2
		//print_mdata_raw(moveArray[ind]);
	}

	for(int ind = 0; ind < BOARD_SPACE_NUM; ind++){
		for(int clique = 0; clique < 3; clique++){
			for(int cliqueInd = 0; cliqueInd < BOARD_LEN; cliqueInd++){
				temp = board_get_val(board,CLIQUE_INDS[CLIQUE_VAL_DICT[ind][clique]][cliqueInd]);
				moveArray[ind] = set_mdata_val(moveArray[ind],temp);
			}
		}
	}

	return moveArray;
}

num_t* create_move_num_list(mdata_t* moveArray){
	num_t* moveNumArray = calloc(BOARD_SPACE_NUM,sizeof(num_t));
	mdata_t temp;

	for(int ind = 0; ind < BOARD_SPACE_NUM; ind++){
		temp = moveArray[ind];
		for(int n = 0; n < BOARD_LEN; n++){
			if((temp & 512) == 512) moveNumArray[ind] += 1;
			temp <<= 1;
		}
	}

	return moveNumArray;
}

void print_moves_at_ind(mdata_t* moveArray, num_t* moveNumArray, int ind){
	if(moveNumArray[ind]){
		printf("Ind: [%d]\tMove Num: [%d]\tVals: ",ind,moveNumArray[ind]);
		for(int val = 1; val <= BOARD_LEN; val++){
			if(get_mdata_val(moveArray[ind],val)) printf("%d ", val);
		}
		printf("\n");
	}
}

void print_moves_list(mdata_t* moveArray, num_t* moveNumArray){

	for(int ind = 0; ind < BOARD_SPACE_NUM; ind++){
		if(moveNumArray[ind]){
			printf("Ind: [%d]\tMove Num: [%d]\tVals: ",ind,moveNumArray[ind]);
			for(int val = 1; val <= BOARD_LEN; val++){
				if(get_mdata_val(moveArray[ind],val)) printf("%d ", val);
			}
			printf("\n");
		}
	}
}

void update_moves_list(mdata_t* moveArray, num_t* moveNumArray, int ind, int val){

	int tempInd;
	mdata_t oldMData;

	for(int clique = 0; clique < 3; clique++){
		for(int cliqueInd = 0; cliqueInd < BOARD_LEN; cliqueInd++){
			tempInd = CLIQUE_INDS[CLIQUE_VAL_DICT[ind][clique]][cliqueInd];
			if(get_mdata_val(moveArray[tempInd],val)) moveNumArray[tempInd]--; //If you haven't updated the num of moves, update it
			moveArray[tempInd] = set_mdata_val(moveArray[tempInd],val); //Remove val from possible moves
		}
	}
}

void board_do_move(num_t* board, mdata_t* moveArray, num_t* moveNumArray, int ind, int val){
	board_set_val(board,ind,val);
	update_moves_list(moveArray,moveNumArray,ind,val);
}

int check_if_move_valid(num_t* board, mdata_t* moveArray, int ind, int val){
	if(val < 1 || val > BOARD_LEN) return 0; //Val must be between 1 and 9 (inclusive)
	else if (ind < 0 || ind >= BOARD_SPACE_NUM) return 0; //Index must be on the board
	else if (board_get_val(board,ind)) return 0; //There has to be nothing on that place at the board
	else return get_mdata_val(moveArray[ind],val); //Finally, check if that is a possible move at this position
}

//Just iterate through the board and find places where there is only one possible move, do that move, and repeat until you can't find any
void do_forced_moves(num_t* board, mdata_t* moveArray, num_t* moveNumArray, int startInd){

	int hasForcedMoves;

	do {
		hasForcedMoves = 0;
		for(int ind = startInd; ind < BOARD_SPACE_NUM; ind++){

			if(moveNumArray[ind] == 1 && !board_get_val(board,ind)){
				for(int val = 1; val <= BOARD_LEN; val++){
					if(check_if_move_valid(board,moveArray,ind,val)){

						board_do_move(board,moveArray,moveNumArray,ind,val);

						hasForcedMoves = 1;
						break;
					}
				}
				break;
			}

		}
	} while (hasForcedMoves);
}

//If, in a clique, there is a place where there is only one place that a number could possibly go, put that number there, and repeat until no more of these cases are found
void do_assumed_moves(num_t* board, mdata_t* moveArray, num_t* moveNumArray){
	int hasAssumedMoves, ind, hasMove;
	mdata_t temp;
	num_t cliqueMoveNums[BOARD_LEN+1]; //Number of each type of move that can be done
	int cliqueMoveInds[BOARD_LEN+1]; //Indicies of places where a certain type of move first appeared

	do {
		hasAssumedMoves = 0;
		for(int clique = 0; clique < CLIQUE_NUM; clique++){

			memset(cliqueMoveNums,0,sizeof(num_t) * (BOARD_LEN+1));
			memset(cliqueMoveInds,0,sizeof(int) * (BOARD_LEN+1));

			for(int cliqueInd = 0; cliqueInd < BOARD_LEN; cliqueInd++){

				ind = CLIQUE_INDS[clique][cliqueInd];
				temp = moveArray[ind];

				if(!board_get_val(board,ind)){
					for(int val = 1; val <= BOARD_LEN; val++){
						if((temp & 2)) hasMove = 1;
						else hasMove = 0;

						if(!cliqueMoveNums[val] && hasMove) cliqueMoveInds[val] = ind;
						cliqueMoveNums[val] += hasMove;

						temp >>= 1;
					}
				}

			}

			for(int val = 1; val <= BOARD_LEN; val++){
				if(cliqueMoveNums[val] == 1){

					//printf("Assumed move [%d] found at ind [%d]\n",val,cliqueMoveInds[ind]);
					board_do_move(board,moveArray,moveNumArray,cliqueMoveInds[val],val);
					hasAssumedMoves = 1;
				}
			}

			if(hasAssumedMoves) break;
		}
		
	} while (hasAssumedMoves);
}

//Find hidden pairs, and use those hidden pairs to eliminate some moves
void find_hidden_pairs(num_t* board, mdata_t* moveArray, num_t* moveNumArray){

	num_t cliqueMoveNums[BOARD_LEN+1];
	int cliqueMoveInds1[BOARD_LEN+1];
	int cliqueMoveInds2[BOARD_LEN+1];
	int ind, v1, v2, i1, i2;

	mdata_t temp;
	int hasMove, hasHiddenPairs, pairNum;

	do {
		hasHiddenPairs = 0;

		for(int clique = 0; clique < CLIQUE_NUM; clique++){

			pairNum = v1 = v2 = 0;

			memset(cliqueMoveNums,0,sizeof(num_t) * (BOARD_LEN+1));
			memset(cliqueMoveInds1,0,sizeof(int) * (BOARD_LEN+1));
			memset(cliqueMoveInds2,0,sizeof(int) * (BOARD_LEN+1));

			for(int cliqueInd = 0; cliqueInd < BOARD_LEN; cliqueInd++){

				ind = CLIQUE_INDS[clique][cliqueInd];
				temp = moveArray[ind];

				if(!board_get_val(board,ind)){
					for(int val = 1; val <= BOARD_LEN; val++){
						if((temp & 2)) hasMove = 1;
						else hasMove = 0;

						if(!cliqueMoveNums[val] && hasMove) cliqueMoveInds1[val] = ind;
						else if((cliqueMoveNums[val] == 1) && hasMove) cliqueMoveInds2[val] = ind;
						cliqueMoveNums[val] += hasMove;

						temp >>= 1;
					}
				}
			}

			for(int val = 1; val <= BOARD_LEN; val++){
				if(cliqueMoveNums[val] == 2){
					if(!v1) v1 = val;
					else v2 = val;
				}
				if(v2) break;
			}

			if(v2 && cliqueMoveInds1[v1] == cliqueMoveInds1[v2] && cliqueMoveInds2[v1] == cliqueMoveInds2[v2]){

				i1 = cliqueMoveInds1[v1];
				i2 = cliqueMoveInds2[v2];

				if(moveNumArray[i1] > 2 && moveNumArray[i1] > 2){
					for(int val = 1; val <= BOARD_LEN; val++){
						if(val != v1 && val != v2){
							if(get_mdata_val(moveArray[i1],val)) moveNumArray[i1]--;
							moveArray[i1] = set_mdata_val(moveArray[i1],val);

							if(get_mdata_val(moveArray[i2],val)) moveNumArray[i2]--;
							moveArray[i2] = set_mdata_val(moveArray[i2],val);
						}
					}
					hasHiddenPairs = 1;
				}
			}

		}
	} while (hasHiddenPairs);
}

int check_board_validity(num_t* board){
	int 

	for(int clique = 0; clique < CLIQUE_NUM; clique++){
		
	}
}

int solve_board(num_t* board, mdata_t* moveArray, num_t* moveNumArray, int ind){

	//printf("\n");
	//print_board(board);
	//print_moves_list(moveArray,moveNumArray);

	num_t newBoard[BOARD_SPACE_NUM];
	mdata_t newMovesArray[BOARD_SPACE_NUM];
	num_t newMoveNumArray[BOARD_SPACE_NUM];

	//First, do all the forced moves (places where it's only possible to put 1 number)
	do_forced_moves(board,moveArray,moveNumArray,ind);
	//printf("Forced moves done\n");
	//print_board(board);

	//Then, find all the hidden pairs, and weed out moves that don't matter
	//find_hidden_pairs(board,moveArray,moveNumArray);
	//printf("Hidden pairs found\n");

	//Then, do all the assumed moves (a bit more complicated, but similar to what forced moves are)
	do_assumed_moves(board,moveArray,moveNumArray);
	//printf("Assumed moves done\n");
	//print_board(board);

	//Then, update the current ind until you find an empty space
	while(ind < BOARD_SPACE_NUM && board_get_val(board,ind)) ind++;

	//If you can't find an empty space, the board is solved
	if(ind >= BOARD_SPACE_NUM){
		memcpy(finalBoard,board,BOARD_SPACE_NUM*sizeof(num_t));
		return 1;
	}

	//If you did, and there are possible moves to be done at that location, start guessing
	else if (moveNumArray[ind]){

		for(int val = 1; val <= BOARD_LEN; val++){
			if(check_if_move_valid(board,moveArray,ind,val)){

				memcpy(newBoard,board,BOARD_SPACE_NUM*sizeof(num_t));
				memcpy(newMovesArray,moveArray,BOARD_SPACE_NUM*sizeof(mdata_t));
				memcpy(newMoveNumArray,moveNumArray,BOARD_SPACE_NUM*sizeof(num_t));

				//printf("Trying out move [%d] at ind [%d]\n", val, ind);

				board_do_move(newBoard,newMovesArray,newMoveNumArray,ind,val);

				if(solve_board(newBoard,newMovesArray,newMoveNumArray,ind+1)) return 1;
			}
		}
	} else { //If there aren't any possible moves at that empty space, you messed up, so start backtracking
		//printf("Backtracking...\n");
		backtracks++;
	}

	return 0;
}

void set_board_from_file(FILE* fp, char* boardName, num_t* board){
	char buffer[8192];
	int foundBoard = 0;

	int boardToAdd[9] = {0,0,0,0,0,0,0,0,0};
	int currentInd = 0;
	int boardNameLen = strlen(boardName);

	while(fgets(buffer,8192,fp)){
		if(!strncmp(buffer,boardName,boardNameLen)){
			for(int line = 0; line < BOARD_LEN; line++){
				fgets(buffer,8192,fp);
				sscanf(buffer,"%d,%d,%d,%d,%d,%d,%d,%d,%d",
					boardToAdd,
					boardToAdd+1,
					boardToAdd+2,
					boardToAdd+3,
					boardToAdd+4,
					boardToAdd+5,
					boardToAdd+6,
					boardToAdd+7,
					boardToAdd+8);

				for(int ind = 0; ind < BOARD_LEN; ind++) board_set_val(board,currentInd+ind,boardToAdd[ind]);
				currentInd += BOARD_LEN;
			}
			foundBoard = 1;
		}
	}

	if(!foundBoard){
		printf("Board [%s] not found!\n",boardName);
	}
}

int get_current_milliseconds(){
	struct timespec spec;
	int s, ms;

	clock_gettime(CLOCK_REALTIME,&spec);
	s = spec.tv_sec;
	ms = (int)(spec.tv_nsec / 1e6);

	if(ms > 999){
		s++;
		ms = 0;
	}

	return s*1000 + ms;
}

int main(int argc, char** argv){

	num_t* board = create_empty_board();
	mdata_t* moveArray;
	num_t* moveNumArray;
	int startTime, endTime, solutionFound;

	FILE* fIn = fopen(argv[1],"r");
	FILE* fOut = fopen(argv[2],"w");
	set_board_from_file(fIn,argv[3],board);

	moveArray = create_moves_list(board);
	moveNumArray = create_move_num_list(moveArray);

	finalBoard = malloc(BOARD_SPACE_NUM*sizeof(num_t));
	memcpy(finalBoard,board,BOARD_SPACE_NUM*sizeof(num_t));

	startTime = get_current_milliseconds();
	solutionFound = solve_board(board,moveArray,moveNumArray,0);
	endTime = get_current_milliseconds();
	print_board(finalBoard);
	//print_moves_list(moveArray);
	printf("Backtracks: %d\tTime elapsed: %dms\n", backtracks, endTime-startTime);

	//printf("%d\n",check_if_move_valid(board,0,6));

	/*int** cliques;
	cliques = get_cliques(board);
	for (int clique = 0; clique < CLIQUE_NUM; clique++) print_clique(cliques[clique]);
	free_cliques(cliques);*/

	fclose(fOut);
	fclose(fIn);
	free(board);
	free(moveArray);
	free(moveNumArray);
	free(finalBoard);
	//free_moves_list(moveArray);
	
	return 0;
}