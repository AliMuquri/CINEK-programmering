import java.io.*;
import java.net.*;
import java.util.regex.*;
import java.lang.Math;


// class ServerClientThread extends Thread {
//  Socket serverClient;
//  int clientNo;
//  ServerClientThread(Socket inSocket,int counter){
//  serverClient = inSocket;
//   clientNo=counter;
// }
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

    public static int randomNr() throws IOException{
        int lb=1;
        int ub=100;
        int nr =(int )(Math.random() * ub+lb);
        return nr;
    }


    public static void main(String[] args) {
        new Server();
    }


    public Server() {
        String[] clientsId=new String[10];
        int[][] clientsInfo=new int[10][4];

        int nrCli=0;
        try (ServerSocket serverSocket = new ServerSocket(this.port)) {
            System.out.println("Listening on port: " + this.port);
            

            while (true) {

                try (Socket socket = serverSocket.accept();
                    // ServerClientThread sct = new ServerClientThread(socket,nrCli);
                    // sct.start();
                     BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                     BufferedWriter out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()))) {


                    String line;
                    while ((line = in.readLine()) != null) { // read

                        if (line.matches("GET\\s+.*")) {
                            System.out.println(" <<<" + "GET");
                            int cha;
                            String fullbody="";
                            while((cha=in.read())!=-1){
                                fullbody+=(char)cha;

                                if (in.ready()!=true){
                                    break;
                                }
                            }
                            System.out.println(fullbody);
                            String[] splitted= fullbody.split("sessionId=");

                            String payload=readFile("guess.html");
                            payload=payload.replaceAll("%body", "Welcome to the Number Guess Game.<br>Guess a number between 1 and 100");
                            String response;
                            if (splitted.length==1){
                                nrCli++;
                                int low=1;
                                int high=100;
                                int randomNr= randomNr();
                                int counter=0;
                                response= "HTTP/1.1 200 OK\nSet-cookie: sessionId=" +nrCli+ "\nDate:Mon, 15 Jan 2018 22:14:15 GMT\nContent-Length: "+payload.length()+"\nConnection: Keep-alive\nContent-Type: text/html\n\n";
                                response+=payload;
                                clientsInfo[nrCli-1][0]=low;
                                clientsInfo[nrCli-1][1]=high;
                                clientsInfo[nrCli-1][2]=randomNr;
                                clientsInfo[nrCli-1][3]=counter;


                            }else{
                                response= clientsId[Integer.parseInt(splitted[1].trim())-1];
                            }
                            clientsId[nrCli-1]=response;
                            System.out.println(" >>> " + "HTTP RESPONSE");
                            System.out.println(response);
                            out.append(response);
                            out.flush();

                        } else if (line.matches("POST\\s+.*")) {
                            System.out.print("<<<< POST\n");
                            String payload=readFile("guess.html");
                            int cha;
                            String fullbody="";
                            while((cha=in.read())!=-1){
                                fullbody+=(char)cha;

                                if (in.ready()!=true){
                                    break;
                                }
                            }
                            System.out.println(fullbody);
                            String[] splits= fullbody.split("gissadeTalet=");
                            String[] splitted= splits[0].split("sessionId=");


                            int low=clientsInfo[nrCli-1][0];
                            int high=clientsInfo[nrCli-1][1];
                            int randomNr=clientsInfo[nrCli-1][2];
                            int counter=clientsInfo[nrCli-1][3];


                            int gissadeTalet=0;
                            boolean check=true;
                            String response= "HTTP/1.1 200 OK\nSet-cookie: sessionId=" +splitted[1].trim()+"\nDate:Mon, 15 Jan 2018 22:14:15 GMT\nContent-Length: "+payload.length()+"\nConnection: Keep-alive\nContent-Type: text/html\n\n";
                            // //om det är inte ett heltal
                            try
                                    {
                                      // the String to int conversion happens here
                                      gissadeTalet = Integer.parseInt(splits[1]);

                                      if (gissadeTalet>randomNr && gissadeTalet<high){
                                          counter+=1;
                                          high=gissadeTalet;
                                          payload=payload.replaceAll("%body", "Nope, guess a number between " + low + " and " + high+ "<br> You have made " + counter + " guesses");

                                      }else if (gissadeTalet<randomNr && gissadeTalet>low){
                                          counter+=1;
                                          low=gissadeTalet;
                                          payload=payload.replaceAll("%body", "Nope, guess a number between " + low +" and " + high + "<br> You have made " + counter + " guesses");

                                      }else if(gissadeTalet==randomNr){

                                          check=false;
                                          counter++;
                                          clientsId[nrCli-1]=null;
                                          clientsInfo[nrCli-1][0]=0;
                                          clientsInfo[nrCli-1][1]=0;
                                          clientsInfo[nrCli-1][2]=0;
                                          clientsInfo[nrCli-1][3]=0;
                                          payload=payload.replaceAll("%body", "You made it!! You have made " + counter + " guesses <br> <p><a href=\"http://localhost:8989/\"> New Game</a></p>");
                                          response="HTTP/1.1 200 OK\nSet-cookie: sessionId=" +nrCli+"  ;expires=Mon, 05 Januari 2000 00:00:00 GMT\n 2000Date:Mon, 15 Jan 2018 22:14:15 GMT\nContent-Length: "+payload.length()+"\nConnection: close\nContent-Type: text/html\n\n";
                                          response+=payload;
                                          System.out.println(response);
                                          out.append(response);
                                          out.flush();

                                      }else if(gissadeTalet<=1 || gissadeTalet>=100){
                                          NumberFormatException nfe = new NumberFormatException();
                                          throw nfe;
                                      }else{
                                          check=false;
                                      }
                                    }
                                    catch (NumberFormatException nfe){
                                        payload=payload.replaceAll("%body", "Only numbers between " + low + " and " + high +", try again! ");
                                    }


                            if (check){

                                response+=payload;
                                clientsId[nrCli-1]=response;
                                clientsInfo[nrCli-1][0]=low;
                                clientsInfo[nrCli-1][1]=high;
                                clientsInfo[nrCli-1][2]=randomNr;
                                clientsInfo[nrCli-1][3]=counter;
                                System.out.println(" >>> " + "HTTP RESPONSE");
                                System.out.println(response);
                                out.append(response);
                                out.flush();
                            }

                        }
                    }


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
