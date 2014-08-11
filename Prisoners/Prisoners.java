import java.util.Random; 

/**
 * An evolutionary algorithm that finds optimal or close to optimal
 * strategies for Iterated Prisoner's Dilemma. Given enough iterations,
 * population should converge to individuals playing the Tit-for-Tat 
 * strategy, which is to cooperate first and copy your opponent's last
 * move on every subsequent move. 
 * Cooperate : Prisoner stays silent, Defect : Prisoner confesses
 * 
 * Written by Luke Benning
 * Last updated : August 9th, 2014
 * 
 * */
public class Prisoners {

	// Suppress default constructor
	private Prisoners() {}

	// Population Size
	private static int POP_SIZE = 10;
	// Mutation Rate
	private static double MUT_RATE = 0.005;
	// Number of generations to simulate
	private static int GEN_CT = 50000;
	// Rate at which DNA is recombined
	private static double RECOMB_RATE = 0.8;
	// Number of moves back an agent can consider
	private static int HIST_LENGTH = 2;

	// Agent Payoffs
	// C = Cooperate, D = Defect
	// For the binary strings, 0 is cooperate and 1 is defect
	private final static int CD = 0;
	private final static int CC = 3;
	private final static int DC = 5;
	private final static int DD = 1;
	
	// Update interval
	private final static int INTERVAL = 10000;

	/**
	* Entrypoint of simulation - can accept arguments as follows or use defaults
	* (no arguments given)
	* arg1 : population size p
	* arg2 : mutation rate m
	* arg3 : generation count g
	* arg4 : recombination rate r
	* arg5 : historical length l
	*/
	public static void main(String args[]) {
		// If arguments given, use them if valid else exit, otherwise use defaults
		if (args.length == 5) {
			Prisoners.parseArgs(args);
		}
		else if (args.length != 0) {
			System.out.println("Malformed arguments, either provide all 5 args. or give none to use default parameters");
			System.exit(0);
		}
		// Begin simulation
		final int[][] population = simulate();
	}

	/**
	* Simulates iterated Prisoner's Dilemma
	*/
	public static int[][] simulate() {

	    int[][] agents = initAgents();
		final Random rand = new Random(); 

		// Run over all generations
		for (int gen = 0; gen < GEN_CT; gen++) {
			int[] points = new int[agents.length];
			final int games = rand.nextInt(45) + HIST_LENGTH+5;
			// Tournament rounds
			for (int p1 = 0; p1 < agents.length-1; p1++) {
				for (int p2 = p1+1; p2 < agents.length; p2++) {

					// Choice arrays
					final int[] p1Hist = new int[games];
					final int[] p2Hist = new int[games];

					// Handle zeroth round
					points[p1] += scorer(agents[p1][0], agents[p2][0]);
					points[p2] += scorer(agents[p2][0], agents[p1][0]);
					p1Hist[0] = agents[p1][0];
					p2Hist[0] = agents[p2][0];

					// Handle rounds 1,2,...,HIST_LENGTH-1
					for (int i = 1; i < HIST_LENGTH; i++) {
						int index1 = (int)(Math.pow(2,i+1)-2);
						int index2 = (int)(Math.pow(2,i+1)-2);
						int factor = 1;
						for (int j = i; j > 0; j--) {
							index1 -= agents[p2][j]*factor;
							index2 -= agents[p1][j]*factor;
							factor *= 2;
						}
						points[p1] += scorer(agents[p1][index1], agents[p2][index2]);
						points[p2] += scorer(agents[p2][index2], agents[p1][index1]);
						p1Hist[i] = agents[p1][index1];
						p2Hist[i] = agents[p2][index2];
					}

					// Handle rounds HIST_LENGTH, HIST_LENGTH+1, ..., games-1
					for (int i = HIST_LENGTH; i < games; i++) {
						// p1 index
						int p1Dex = agents[p1].length-1;
						// p2 index
						int p2Dex = agents[p2].length-1;
						int factor = 1;
						for (int j = 0; j < HIST_LENGTH; j++) {
							p1Dex -= p1Hist[j]*factor;
							p2Dex -= p2Hist[j]*factor;
							factor *= 2;
						}
						for (int j = 0; j < HIST_LENGTH; j++) {
							p1Dex -= p2Hist[j]*factor;
							p2Dex -= p1Hist[j]*factor;
							factor *= 2;
						}
						points[p1] += scorer(agents[p1][p1Dex], agents[p2][p2Dex]);
						points[p2] += scorer(agents[p2][p2Dex], agents[p1][p1Dex]);
						p1Hist[i] = agents[p1][p1Dex];
						p2Hist[i] = agents[p2][p2Dex];
					}	
				}
			}
			// Post tournament processing
			final int totalPoints = sumPoints(points);
			
			// Reproduction stage
			final int offSpringCount = (int)RECOMB_RATE*POP_SIZE;
		    int[][] offSpring = new int[agents.length][agents[0].length];
			for (int x = 0; x < offSpringCount; x++) {
				// Select parents - Possible for asexual reproduction
				final int parentX = parentSearch(rand.nextInt(totalPoints), points);
				final int parentY = parentSearch(rand.nextInt(totalPoints), points);
				offSpring[x] = reproduce(agents[parentX], agents[parentY]);
			}
			// Select POP_SIZE - offSpringCount individuals from population to endure, based on scores
			for (int y = offSpringCount; y < offSpring.length; y++) {
				offSpring[y] = agents[parentSearch(rand.nextInt(totalPoints), points)];
			}
			// Update the population
			agents = offSpring;	
			if (gen % INTERVAL == 0) {
				System.out.println("Generation " + gen + " complete!");
			} 
		}
		return agents;
	}

	/**
	* @return A 2d array containing POP_SIZE agents, each with
	* strategy arrays of length 4^(HIST_LENGTH)+2^(HIST_LENGTH+1)-1
	*/
	private static int[][] initAgents() {
		final Random rand = new Random(); 
		// compute length of bitstring to handle all possible outcomes - this will be used to
		// form a strategy array
		final int bitLength = (int)(Math.pow(4.0, HIST_LENGTH)+Math.pow(2, HIST_LENGTH)-1);
		final int[][] agents = new int[POP_SIZE][bitLength];
		for (int i = 0; i < agents.length; i++) {
			for (int j = 0; j < agents[i].length; j++) {
				agents[i][j] = rand.nextInt(2);
			}
		}
		return agents;
	}

	/**
	* Parses command line arguments. If arguments are malformed,
	* prints a message and exits Prisoners.
	* 
	* Dependent types on arguments : Z is integers, D is doubles
	* arg1 : population size p : {p ∈ Z | p > 1}
	* arg2 : mutation rate m : {m ∈ D | 0 < m < 1}
	* arg3 : generation count g : {g ∈ Z | g > 0}
	* arg4 : recombination rate r : {r ∈ D | 0 < r < 1 && p*r = ceil(p*r)}
	* arg5 : historical length l : {l ∈ Z | l > 1}
	*/
	private static void parseArgs(final String[] args) {
		try {
			final int p = Integer.parseInt(args[0]);
			if (p > 1) { POP_SIZE = p; }
			final double m = Double.parseDouble(args[1]);
			if (m > 0 && m < 1) { MUT_RATE = m; }
			final int g = Integer.parseInt(args[2]);
			if (g > 0) { GEN_CT = g; }
			final double r = Double.parseDouble(args[3]);
			if (r > 0 && r < 1 && r*p == Math.ceil(r*p)) { RECOMB_RATE = r; }
			final int h = Integer.parseInt(args[4]);
			if (h > 0) { HIST_LENGTH = h; }
			System.out.println("Successfully parsed arguments!");
		}
		catch(Exception e) {
			System.out.println("Failed to parse arguments, please check input.");
			System.exit(0);
		}
	}

	/**
	* resX and resY are choices, points computed for resX
	* @return Score to be added to agent X
	*/
	private static int scorer(final int resX, final int resY) {
		if (resX == 1 && resY == 1) { return DD; }
		else if (resX == 1) { return DC; }
		else if (resY == 1) { return CD; }
		return CC;
	}

	/**
	* Sums integer array
	* @return integer sum of points
	*/
	private static int sumPoints(final int[] input) {
		int sum = 0;
		for (int x : input) { sum += x; }
		return sum;
	}
	
	/**
	 * find index x such that sum(i=0,...,x-1) points[i] <= target < 
	 * sum(j=0,...,x) points[j]
	 * @return index of individual in points selected by target
	 */
	private static final int parentSearch(final int target, final int[] points) {
		int x = target;
		int index = 0;
		while (x - points[index] >= 0) {
			x -= points[index];
			index++;
		}
		return index;
	}
	
	/** 
	 * @return bitstring for reproduced individual from given parents
	 */
	 private static int[] reproduce(final int[] parentX, final int[] parentY) {
		 final Random rand = new Random();
		 final int[] child = new int[parentX.length];
		 final int divide = rand.nextInt(parentY.length-9) + 5;
		 // Add parentX genetic data
		 for (int x = 0; x < divide; x++) {
			 child[x] = parentX[x];
		 }
		 // Add parentY genetic data
		 for (int x = divide; x < parentX.length; x++) {
			 child[x] = parentY[x];
		 }
		 // With probability MUT_RATE, perform mutation on child
		 if (rand.nextInt((int)(1.0/MUT_RATE)) == 0) {
			 mutate(child);
		 }
		 return child;
	 }
	 
	 /**
	  * @return child with mutation performed
	  */
	  private static void mutate(final int[] child) {
		  final Random rand = new Random();
		  final int base = rand.nextInt(child.length-4);
		  for (int x = base; x <= base + 5; x++) {
			  child[x] = rand.nextInt(2);
		  }
	  }
}