import java.io.*;
import java.net.*;
import java.util.regex.*;
import java.lang.Math;
import java.util.ArrayList;

public class Server{
    public static void main(String args[]) {
        try (ServerSocket serverSocket = new ServerSocket(8989)) {
            System.out.println("Listening on port: " + 8989);
            while (true) {
                //skapar nya objekt
                try {Socket sock = serverSocket.accept();
                    ClientH handler = new ClientH(sock);
                    Thread thread = new Thread(handler);
                    thread.start();
                } catch (IOException e) {
                    System.err.println(e.getMessage());
                }
            }
        }catch (IOException e) {
            System.err.println(e.getMessage());
            System.err.println("Could not listen on port: " + 8989);
            System.exit(1);
        }
    }
}
//Konstrukturn initialiseras för varje session samma data fast en annan sessionsId
public class Session{
    private int sessionId=0;
    private int low;
    private int high;
    private int randomNr;
    private int counter;
    private static int antal;
    private String lastpayload;

    public Session() throws IOException{
            this.sessionId=antal;
            antal++;
            this.randomNr=(int )(Math.random() * 100+1);
            this.low=1;
            this.high=100;
            this.counter=0;
        }

    public int guesses(String gissning){

        try
        {
            int gissadeTalet;
            // the String to int conversion happens here
            gissadeTalet = Integer.parseInt(gissning);
            if (gissadeTalet>randomNr && gissadeTalet<high){
                counter++;
                high=gissadeTalet;
                return 1;
            }else if(gissadeTalet<randomNr && gissadeTalet>low){
                counter++;
                low=gissadeTalet;
                return 2;
            }else if(gissadeTalet==randomNr){
                counter++;
                return 0;
            }else if(gissadeTalet<=1 || gissadeTalet>=100){
                return 3;
            }
        }catch (NumberFormatException nfe){
            return 3;
        }
        return 3;
    }


    //Andra hjälpmetoder
    public int sId(){
        return sessionId;
    }
    public int giveCount(){
        return counter;
    }
    public int giveLow(){
        return low;
    }
    public int giveHigh(){
        return high;
    }
    public String lastPayL(){
        return lastpayload;
    }
    public void setlastPayL(String payload){
        this.lastpayload=payload;
    }
    public void WIN(){

        randomNr=(int )(Math.random() * 100+1);
        low=1;
        high=100;
        counter=0;
        lastpayload="";
    }

}
public class ClientH implements Runnable {
    private Socket socket;
    private BufferedReader in;
    private BufferedWriter out;
    private static ArrayList<Session> sessions = new ArrayList<Session>();


    //Varje objekt får i sin konstruktur ett eget socket och egna streams
    public ClientH (Socket socket) throws IOException{
        this.socket=socket;
        in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));

    }
    //Läser in html filen
    public String readFile(String filename)throws IOException{
        BufferedReader file=new BufferedReader(new FileReader(filename));
        String contents ="";
        String line = "";
        while ((line = file.readLine()) != null)
            contents += line;
            return contents;
    }

    @Override
    public void run(){
        try {
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
                String response="";
                Session newSession=null;

                System.out.println(splitted.length);
                // 1) Om det är samma tab så splitted.length>1; 2)Om det är omkörning splitted.length==1;
                for (Session n:sessions){
                    if (splitted.length>1){
                        if (n.sId()==Integer.parseInt(splitted[1].trim())){
                            newSession=n;
                            payload=newSession.lastPayL();
                            break;
                        }
                    }
                }

                // Om newSession är null så skapar vi en ny session och skickar ditt en ny sessionId och clientInfo
                if (newSession==null){
                    System.out.println("REPEAT");
                    newSession= new Session();
                    sessions.add(newSession);
                    payload=payload.replaceAll("%body" ,"Welcome to the Number Guess Game. Guess a number between 1 and 100");
                }

                newSession.setlastPayL(payload);
                response="HTTP/1.1 200 OK\nSet-cookie: sessionId=" +newSession.sId() +"\nDate:Mon, 15 Jan 2020 22:14:15 GMT\nContent-Length: "+payload.length()+"\nConnection: Keep-alive\nContent-Type: text/html\n\n";
                response+=payload;
                System.out.println(" >>> " + "HTTP RESPONSE");
                System.out.println(response);
                out.append(response);
                out.flush();


            } else if (line.matches("POST\\s+.*")) {
                Session newSession = new Session();
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
                String response="";
                boolean win=false;
                for (Session n:sessions){
                    if (n.sId()==Integer.parseInt(splitted[1].trim())){
                        newSession=n;
                    }
                }
                int outcome=newSession.guesses(splits[1]);

                switch(outcome){
                case 1:
                    payload=payload.replaceAll("%body", "Nope, guess a number between " + newSession.giveLow() +" and " + newSession.giveHigh()  + "<br> You have made " + newSession.giveCount()  + " guesses");
                    break;
                case 2:
                    payload=payload.replaceAll("%body", "Nope, guess a number between " + newSession.giveLow()+ " and " + newSession.giveHigh() + "<br> You have made " + newSession.giveCount() + " guesses");
                    break;
                case 3:
                    payload=payload.replaceAll("%body", "Only numbers between " + newSession.giveLow()+ " and " + newSession.giveHigh() +", try again! ");
                    break;
                default:
                    win=true;
                }

                if (win){
                    payload=payload.replaceAll("%body", "You made it!! You have made " + newSession.giveCount() + " guesses <br> <p><a href=\"http://localhost:8989/\"> New Game</a></p>");
                    payload=payload.replaceAll("<form name=\"guessform\" method=\"POST\"><input type=\"text\" name=\"gissadeTalet\" autofocus><input type=\"submit\" value=\"Guess\"></form>","");
                    response="HTTP/1.1 200 OK\nSet-cookie: sessionId=" +newSession.sId()+"  ;expires=Mon, 05 Januari 2000 00:00:00 GMT\n 2000Date:Mon, 15 Jan 2020 22:14:15 GMT\nContent-Length: "+payload.length()+"\nConnection: Close\nContent-Type: text/html\n\n";
                    newSession.WIN();
                    response+=payload;
                }else{

                newSession.setlastPayL(payload);
                response= "HTTP/1.1 200 OK\nSet-cookie: sessionId=" +newSession.sId()+ "\nDate:Mon, 15 Jan 2020 22:14:15 GMT\nContent-Length: "+payload.length()+"\nConnection: Keep-alive\nContent-Type: text/html\n\n";
                response+=payload;
                }

                System.out.println(" >>> " + "HTTP RESPONSE");
                System.out.println(response);
                out.append(response);
                out.flush();

            }
        }
        out.flush(); // flush
    }catch (IOException e) {
        System.out.println(e);
    }
    }
}
