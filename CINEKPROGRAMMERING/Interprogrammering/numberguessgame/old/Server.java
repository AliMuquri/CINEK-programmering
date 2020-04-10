import java.io.*;
import java.net.*;
import java.util.Random;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;


// Skapar servernt
public class Server {
    //Port vi ska lyssna på
    private final int port = 8989;

    public static String readFile(String filename)throws IOException{
	BufferedReader file=new BufferedReader(new FileReader(filename));
	String contents ="";
	String line = "";
	while ((line = file.readLine()) != null)
	    contents += line;
	return contents;
    }

    public static void writeStringToFile(String filename) throws IOException{
        BufferedWriter file=new BufferedWriter(new FileWriter("tempguess.html"));
        file.write(filename);
        file.close();

    }

    //main, där kallar vi Server funktionen
    public static void main(String[] args) {
        new Server();
    }

    //I funktionen använder vi oss av IOException för att fånga fel om porten
    //vi lyssnar på misslyckas.
    public Server() {
        try (ServerSocket serverSocket = new ServerSocket(this.port)) {
            //Om det lyckas så skriver vi ut porten
            System.out.println("Listening on port: " + this.port);
            //Vi loopar får att kontinuerligt fånga kommunikationen
            int number;
            int counter;
            //Request handler loop
            while (true) {
                //Vi kör en IOException här också ifall när vi kallar på .accept() och inget hittas
                try (Socket socket = serverSocket.accept();
                // Dessa fångar/skickar kommunikation från servern via socket.
                     BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                     BufferedWriter out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()))) {

                    String line;
                    //Request-response loop
                    //Läser in vad clienten har skickat
                    while ((line = in.readLine()) != null) { // Läser av första raden av clientens reques

                        System.out.println(" <<< " + line); // log
                        //Om det är request-Get från clientet.

                        if (line.matches("(.*)GET(.*)") {
                            String htmlString=readFile("guess.html");
                            String title="New Pag";
                            String body ="Welcome to the Number Guess Game. Guess a number between 1 and 100";
                            htmlString= htmlString.replaceAll("$title", title);
                            htmlString= htmlString.replaceAll("$body ", body);
                            writeStringToFile(htmlString);


                            //Slumpar är en random nummer
                            //Läser från guess.html filen
                            String payload=readFile("tempguess.html");
                            //Skickare en response från vad som laddes upp från respons filen
                            String response= "HTTP/1.1 200OK\nDate: Mon, 15 Jan 2018 22:14:15 GMT\nContent-Length: "+payload.length()+"\nConnection: close\nContent-Type: text/html\n\n";
                            response+=payload;
                            out.append(response);
                            out.flush();
                        //Om är request-post från clienten.
                        }else if (line.matches("POST\\s+.*")) {

                            //System.out.println(" >>> " + "HTTP RESPONSE"); // log
                            //out.write("HTTP RESPONSE"); // write

                            String payload=readFile("guess.html");
                            String response= "HTTP/1.1 200OK\nDate: Mon, 15 Jan 2018 22:14:15 GMT\nContent-Length: "+payload.length()+"\nConnection: close\nContent-Type: text/html\n\n";
                            response+=payload;
                            out.append(response);
                            //flush påskyndar(inväntar) så allt som ska kommuniceras avslutas innan
                            //vi träder in i nästa looop.
                            out.flush(); // flush
                        }
                    }
                }catch (IOException e) {
                    System.err.println(e.getMessage());
                }
            }
        }catch (IOException e) {
            System.err.println(e.getMessage());
            System.err.println("Could not listen on port: " + this.port);
            System.exit(1);
        }
    }

}
