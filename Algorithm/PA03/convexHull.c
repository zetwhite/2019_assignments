#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>
#define MAX_CO 40000
#define innerYrange(a, b, poly) poly->stackStorage[a]->y < p->y && poly->stackStorage[b]->y > p->y

typedef struct Point {
	long long x;
	long long y;
	double angle;
}Point;

Point* makePoint(long long x, long long y) {
	Point* newPoint = (Point*)malloc(sizeof(Point));
	newPoint->x = x;
	newPoint->y = y;
	return newPoint;
}

//stack�� ���� �����Ͽ� ����Ͽ����ϴ�.
/*
  stack ���� �Լ���
  initStack : stack ����ü�� ����� �� �ֵ��� �ʱ�ȭ ���ִ� �Լ�
  push : stack�� push
  pop : stack�� pop
  top : stack�� top�� ��ȯ���ش�.
  underneathTop : stack�� top�� �ٷ� �Ʒ� ���� ��ȯ���ش�.
*/
typedef struct stack {
	int using_size;
	int index_here;
	Point** stackStorage;
}Stack;

void initStack(int stackSize, Stack* st) {
	st->stackStorage = (Point**)malloc(sizeof(Point*)*stackSize);
	st->index_here = -1;
	st->using_size = 0;
	return;
}

void push(Stack* st, Point * p) {
	st->index_here++;
	st->stackStorage[st->index_here] = p;
	st->using_size++;
	return;
}

Point* pop(Stack* st) {
	Point* p = st->stackStorage[st->index_here];
	st->index_here--;
	st->using_size--;
	return p;
}

Point* top(Stack const* st) {
	return st->stackStorage[st->index_here];
}

Point* underneathTop(Stack const* st) {
	int index = st->index_here - 1;
	return st->stackStorage[index];
}

//outerP : vector1 x vector2 , �� ������ ���� ���� ��ȯ���ִ� �Լ�
long long outerP(const Point* vector1, const Point* vector2) {
	return vector1->x*vector2->y - vector1->y*vector2->x;
}

//getDistance1 : point a, point b ������ �Ÿ��� �������� ��ȯ���ִ� �Լ�
long long getDistance1(const Point* a, const Point* b) {
	return (a->x - b->x)*(a->x - b->x) + (a->y - b->y)*(a->y - b->y);
}

Point* gLowest_p;

//compare : point a�� angle�� b�� angle���� ũ�ٸ� true ��ȯ, �� ���� ��� else��ȯ
int compare(const void* a, const void* b) {
	Point** first = (Point**)a;
	Point** second = (Point**)b;
	if ((*first)->angle >= (*second)->angle)
			return 1;
	else
		return -1;
}

//distance�� ���� �������ִ� �Լ�
void sortByDistance(Point** pointStorage, int PointSize) {
	for (int i = 0; i < PointSize - 1; i++) {
		if (pointStorage[i]->angle == pointStorage[i + 1]->angle) {
			if (getDistance1(gLowest_p, pointStorage[i]) >= getDistance1(gLowest_p, pointStorage[i + 1])) {
				Point* tmp = pointStorage[i];
				pointStorage[i] = pointStorage[i + 1];
				pointStorage[i + 1] = tmp;
			}
		}
	}
}

void memoryFree(Point** pointStorage, int PointSize) {
	for (int i = 0; i < PointSize; i++) {
		free(pointStorage[i]);
	}
	free(pointStorage);
}

//printStack : stack�� �����ִ� ������ ������ִ� �Լ�
void printStack(Stack* st, FILE *out){
  printf("convex hull : \n");
  fprintf(out, "convex hull : \n");
  for(int i = 0; i < st->using_size; i++){
    printf("%lld %lld\n", st->stackStorage[i]->x, st->stackStorage[i]->y);
    fprintf(out, "%lld %lld\n", st->stackStorage[i]->x, st->stackStorage[i]->y);
  }
}

//isInside : Stack* poly�� ��Ÿ���� �ٰ����� point p�� ���ԵǴ��� ���ο� ��ġ�ϸ� 1 ��ȯ, �ܺ�/���� ���� ��ġ�ϸ� 0��ȯ���ִ� �Լ�
int isInside(Stack* poly, Point* p){
  int crossConnection = 0;
  for (int i = 0; i < poly->using_size-1; i++){
    if(innerYrange(i, i+1, poly)||innerYrange(i+1, i, poly)){
      Point* p1 = poly->stackStorage[i];
      Point* p2 = poly->stackStorage[i+1];
      double x = ((double)(p2->x - p1->x))/(p2->y- p1->y)*(p->y - p1->y) + p1->x;
      if(x > p->x)
        crossConnection++;
    }
    else
      continue;
  }
  if(innerYrange(0, poly->using_size-1, poly) || innerYrange(poly->using_size-1, 0, poly)){
    Point* p1 = poly->stackStorage[0];
    Point* p2 = poly->stackStorage[poly->using_size-1];
    double x = ((double)(p2->x - p1->x))/(p2->y- p1->y)*(p->y - p1->y) + p1->x;
    if(x > p->x)
      crossConnection++;
  }
  if(crossConnection == 1)
    return 1;
  else
    return 0;
}

//getAngle : gLowest_p�� �������� angle�� �����ִ� �Լ�
void getAngle(int PointNumber, Point** pointStorage){
  	for (int i = 0; i < PointNumber; i++) {
		if (pointStorage[i] == gLowest_p) {
			pointStorage[i]->angle = -DBL_MAX;
		}
		else {
			long long dif_x = pointStorage[i]->x - gLowest_p->x;
			long long dif_y = pointStorage[i]->y - gLowest_p->y;
			pointStorage[i]->angle = atan2(dif_y, dif_x);
		}
	}
}

//findConvexHull : pointStorage�� �����տ��� convexHull�� ã�� �Լ�, convexHull�� ���ԵǴ� ���� Stack* convexHull�� ����Ǿ� ��ȯ�ȴ�.
void findConvexHull(int PointNumber, Point** pointStorage, Stack* convexHull){
  getAngle(PointNumber, pointStorage);
  qsort(pointStorage, PointNumber, sizeof(Point*), compare);
	sortByDistance(pointStorage, PointNumber);

	initStack(PointNumber, convexHull);
	push(convexHull, pointStorage[0]);
	push(convexHull, pointStorage[1]);

	Point* lastPushed = top(convexHull);
	Point* vectorOld = makePoint(lastPushed->x - pointStorage[0]->x, lastPushed->y - pointStorage[0]->y);
	Point* vectorYoung;

	for (int i = 2; i < PointNumber; ) {
		vectorYoung = makePoint(pointStorage[i]->x - lastPushed->x, pointStorage[i]->y - lastPushed->y);
		if (outerP(vectorOld, vectorYoung) <= 0) {
			pop(convexHull);
			if (convexHull->using_size == 1) {
				push(convexHull, pointStorage[i]);
				i++;
			}
			lastPushed = top(convexHull);
			vectorOld = makePoint(lastPushed->x - underneathTop(convexHull)->x, lastPushed->y - underneathTop(convexHull)->y);
		}
		else {
			push(convexHull, pointStorage[i]);
			lastPushed = top(convexHull);
			vectorOld = vectorYoung;
			i++;
		}
	}
}


int main(int argv, char* argc[]) {

  //===== in file setting ====
  if(argv < 3){
    printf("too few argument! \n");
    printf("$%s [inputFileName] [ouputFileName]\n", argc[0]);
    return 1;
  }
  FILE* in = NULL;
  in = fopen(argc[1], "r");
  if(in == NULL ){
    printf("input file error\n");
    printf("there is no file named %s", argc[1]);
    return 1;
  }
  //===== out file setting ====
  FILE* out = fopen(argc[2], "w");
  if(out == NULL){
    printf("output file create error\n");
    return 1;
  }

  //==================construct convex Hull========================
	int PointNumber;
	fscanf(in, "%d", &PointNumber);
	Point** pointStorage = (Point**)malloc((sizeof(Point*)*PointNumber+1));
	long long lowest_coY = MAX_CO;
	long long lowest_coX = MAX_CO;

	for (int i = 0; i < PointNumber; i++) { //input �Է� �ޱ�, ���ÿ� ���� ���� �Ʒ��� ��ġ�� ���� ã�� gLowest_p�� �����Ѵ�.
		long long x, y;
		fscanf(in, "%lld %lld", &x, &y);
		pointStorage[i] = makePoint(x, y);
		if (lowest_coY > y) {
			lowest_coY = y;
			lowest_coX = x;
			gLowest_p = pointStorage[i];
		}
		else if (lowest_coY == y && lowest_coX > x) {
			lowest_coX = x;
			gLowest_p = pointStorage[i];
		}
	}

	if (PointNumber == 1){
    printf("only 1 point entered... can not make convex hull\n");
    return 1;
	}

  Stack convexHull;
  findConvexHull(PointNumber, pointStorage, &convexHull); //convexHull ã��
	printStack(&convexHull, out); //convexHull ��� ���

	fflush(in);
	int delim;
	fscanf(in, "%d", &delim);

	//================determine point is in the convex Hull================
	char s;
	fscanf(in, "%s", &s);

	long long x, y;
	fscanf(in, "%lld %lld", &x, &y); //�� P�Է� �ޱ�
	Point* p = makePoint(x, y);
  int res = isInside(&convexHull, p); //�� p�� convexHull ����/�ܺο� ��ġ�ϴ��� �ľ�
  printf("%c=(%lld, %lld) : ",s, p->x, p->y); //��� ���
  fprintf(out,"%c=(%lld, %lld) : ",s, p->x, p->y);
  if(res == 1){
    printf("True\n");
    fprintf(out, "True\n");
  }
  else{
    printf("False\n");
    fprintf(out, "False\n");
  }
	memoryFree(pointStorage, PointNumber);
	return 0;
}
