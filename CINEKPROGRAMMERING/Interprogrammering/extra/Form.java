import java.net.*;
import java.io.*;



class Form{

    
    public static String put_firstname_in_payload(String response_payload,String firstName){
	return response_payload.replace("$first_name$",firstName);
    }

        public static String put_lastname_in_payload(String response_payload,String firstName){
	return response_payload.replace("$last_name$",firstName);
	}
    
    public static String readFile(String filename)throws IOException{
	BufferedReader file=new BufferedReader(new FileReader(filename));
	String contents ="";
	String line = "";
	while ((line = file.readLine()) != null)
	    contents += line;
	return contents;
    }

    
    public static String processTheForm()throws IOException{
	BufferedReader file=new BufferedReader(new FileReader("test.html"));
	String contents ="";
	String line = "";
	while ((line = file.readLine()) != null)
	    contents += line;
	return contents;
    }
    
    public static String readPayload(BufferedReader scktIn,String headers)throws IOException{
	int content_length= Integer.parseInt((((headers.split("Content-Length: "))[1]).split("\n"))[0]);
	char[] cbuf=new char[content_length];
	scktIn.read(cbuf, 0, content_length);
	return new String(cbuf);
    }

    public static void main(String[] args) {
	String firstName="";
	String lastName="";
	ServerSocket ss=null;
	while(true){
	try{
	    if(ss==null)
		ss=new ServerSocket(1234);
	    
	    Socket s=ss.accept();
	    BufferedReader scktIn=new BufferedReader (new InputStreamReader(s.getInputStream()));
	    PrintStream scktOut= new PrintStream(s.getOutputStream());
	    String line=scktIn.readLine();
	    int bytes=0;
	    String headers = "";
	    //läs headern
	    while (!line.equals("")){
		headers += line+"\n";
		line=scktIn.readLine();
	    }
	    //kolla om det gäller GET eller POST
	    if(headers.indexOf("GET") == 0){
		System.out.println("Got a GET-request "+headers+"<");

		String payload=readFile("html_form_forename.html");
		String response= "HTTP/1.1 200 OK\nDate: Mon, 15 Jan 2018 22:14:15 GMT\nContent-Length: "+payload.length()+"\nConnection: close\nContent-Type: text/html\n\n";
		response+=payload;
		scktOut.print(response);
		s.shutdownOutput();
	    }
	    else if(headers.indexOf("POST")==0)
		{
		    System.out.println("Got a POST-request");
		    String request_payload=null;
		    String response_payload=null;
		    
		    if(headers.indexOf("/step1") == 5){
			request_payload = readPayload(scktIn,headers);
			//parsa inmatade förnmanet från requesten och lagra den i variabeln firstName
			firstName = request_payload.substring(request_payload.indexOf("first_name=")+"first_name=".length());
			System.out.println(firstName);
			response_payload=readFile("html_form_lastname.html");
			
		    }else
			if(headers.indexOf("/step2") == 5){
			    request_payload = readPayload(scktIn,headers);
			    //parsa inmatade efternamnet från requesten och lagra den i variabeln lastName
			    lastName = request_payload.substring(request_payload.indexOf("last_name=")+"last_name=".length());
			    System.out.println(lastName);
			    response_payload=readFile("html_form_final.html");
			    response_payload = put_lastname_in_payload(response_payload,lastName);
			}
		    response_payload = put_firstname_in_payload(response_payload,firstName);
		    System.out.println(response_payload);
		    String response= "HTTP/1.1 200 OK\nDate: Mon, 15 Jan 2018 22:14:15 GMT\nContent-Length: "+response_payload.length()+"\nConnection: close\nContent-Type: text/html\n\n";
		    response +=  response_payload;
		    scktOut.print(response);
		    s.shutdownOutput();

		    System.out.println("The payload part of the request:");
		    System.out.println(request_payload);
		}
	    else 
		System.out.println("UNKNOWN REQUEST!");
	    
	}catch (Exception e){
	    e.printStackTrace();
	System.out.println("fel!!!" );
	}

	}
    }
}
