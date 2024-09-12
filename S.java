class S {
    public static void main(String[] args) {
        int[][][] x = {
            {
                {1, 2, 3, 4, 5},
                {3, 4, 5, 6, 7},
                {2, 2, 2, 2, 2}
            },
            {
                {6, 6, 7, 5 ,3},
                {4, 5, 6, 6, 6},
                {6, 5, 3, 5, 6}
            },
            {
                {4, 3, 2, 4, 3},
                {6, 3, 2, 2, 3},
                {5, 7, 9, 8, 0}
            }
        };

        for (int[][] first: x ) {
            for (int[] second: first) {
                for (int third_dimension: second){
                    System.out.println(third_dimension);
                    
                }
            }
        }

    }
}