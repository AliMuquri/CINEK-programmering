import java.io.*;
import java.net.*;


public class Server {

    private final int port = 8989;

    public static String readFile(String filename)throws IOException{
        BufferedReader file=new BufferedReader(new FileReader(filename));
        String contents ="";
        String line = "";
        while ((line = file.readLine()) != null)
            contents += line;
            return contents;
    }




    public static void main(String[] args) {
        new Server();
    }


    public Server() {
        try (ServerSocket serverSocket = new ServerSocket(this.port)) {
            System.out.println("Listening on port: " + this.port);

            while (true) {

                try (Socket socket = serverSocket.accept();
                     BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                     BufferedWriter out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()))) {

                    String line;
                    while ((line = in.readLine()) != null) { // read
                        System.out.println(" <<< " + line); // log

                        if (line.matches("GET\\s+.*")) {
                            String payload=readFile("guess.html");
                            String response= "HTTP/1.1 200 OK\nDate: Mon, 15 Jan 2018 22:14:15 GMT\nContent-Length: "+payload.length()+"\nConnection: close\nContent-Type: text/html\n\n";
                            response+=payload;
                            out.append(response);
                            out.flush();
                            out.close();
                        } else if (line.matches("POST\\s+.*")) {
                            int cha;
                            String fullbody="";
                            while((cha=in.read())!=-1){
                                fullbody+=(char)cha;

                                if (in.ready()!=true){
                                    break;
                                }
                            }
                            System.out.println(fullbody);

                            //System.out.println(gissadeTalet);

                            // process the POST request
                        }
                    }

                    System.out.println(" >>> " + "HTTP RESPONSE"); // log
                    out.write("HTTP RESPONSE"); // write
                    out.flush(); // flush

                } catch (IOException e) {
                    System.err.println(e.getMessage());
                }

            }
        } catch (IOException e) {
            System.err.println(e.getMessage());
            System.err.println("Could not listen on port: " + this.port);
            System.exit(1);
        }
    }

}
