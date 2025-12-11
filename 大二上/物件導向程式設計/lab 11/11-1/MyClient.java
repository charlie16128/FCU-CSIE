	import java.io.*;
	import java.net.Socket;

	public class MyClient {
		private static final String ADDRESS = "127.0.0.1";//ip
		private static final int PORT = 5000;//port
	
		public static void main(String args[]) {
			try {
				Socket client = new Socket(ADDRESS, PORT);
				InputStream in = client.getInputStream();
				OutputStream out = client.getOutputStream();
				
				BufferedReader serverReader = new BufferedReader(new InputStreamReader(in));
				PrintWriter serverwriter = new PrintWriter(out, true);

				Console console = System.console();
				String userInput;
				System.out.print("input: ");
				while ((userInput = console.readLine()) != null) {
					if("-1".equals(userInput)){
						break;
					}
					serverwriter.println(userInput);

					String echoResponse = serverReader.readLine();

					System.out.println(echoResponse);

					System.out.print("input: ");
				}
				client.close();
			} catch(IOException e) {
				System.out.println(e);
			}
		}
	}