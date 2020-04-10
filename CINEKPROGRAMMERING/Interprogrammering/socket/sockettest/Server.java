import java.io.*;
import java.net.*;
public class Server{
public static void main(String[] args) throws Exception{
ServerSocket serverSckt = new ServerSocket(1234);
Socket sckt = null;
while( (sckt = serverSckt.accept()) != null){
BufferedReader indata = new BufferedReader(
new InputStreamReader(sckt.getInputStream()));
String text = null;
while( (text = indata.readLine()) != null){
System.out.println(text);
}
sckt.shutdownInput();
}
}
}
