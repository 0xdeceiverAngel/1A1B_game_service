using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Threading;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Net.WebSockets;
using System.Runtime.Serialization;
using System.Threading;
using Newtonsoft.Json;

namespace _1A1B
{
    /// <summary>
    /// MainWindow.xaml 的互動邏輯
    /// </summary>
    public partial class MainWindow : Window
    {
        public class send_format  // json format 
        {
            public string action { get; set; }
            public string user_guess { get; set; }
            public string send_message { get; set; }
            public string respond_guess { get; set; }
            public string recv_message { get; set; }
            public string creat_room { get; set; }
            public string join_room { get; set; }
        }
        ClientWebSocket client = new ClientWebSocket();

        public MainWindow()
        {
            InitializeComponent();
            initAsync();

        }
        public async void  initAsync()
        {
            var location = new Uri("ws://127.0.0.1:9001"); //connect to server

            //Task taskConnect = client.ConnectAsync(location, null);
            //var cts = new CancellationTokenSource();
            //client.ConnectAsync(location, cts.Token);
            try
            {
                await client.ConnectAsync(location, CancellationToken.None);
            }
            catch
            {
                MessageBox.Show("Connecting lost");
                System.Environment.Exit(0);
            }
            recv();  
        }
        public void send(string data) 
        {
            ArraySegment<byte> buffer = new ArraySegment<byte>(new byte[1024]);
            data = data.Remove(data.Length - 1); // remove string first and last char 
            data = data.Remove(0,1);            // because to pack need to remove '[' and ']'
            //MessageBox.Show(data);
            var encoded = Encoding.UTF8.GetBytes(data);
            var buf = new ArraySegment<Byte>(encoded, 0, encoded.Length);
            client.SendAsync(buf, WebSocketMessageType.Text, true, CancellationToken.None);

        }
       
        public string ConvertByteArrayToString(ArraySegment<Byte>data) //arraysegment to array to string
        {
            var bytes = new byte[data.Count];
            int pos = 0;

            foreach (var b in data)
            {
                bytes[pos] = b;
                pos ++;
            }
            string str = System.Text.Encoding.ASCII.GetString(bytes);
            return str;
        }
        public async void recv()
        {
            try
            {
                ArraySegment<byte> buffer = new ArraySegment<byte>(new byte[1024]);
                WebSocketReceiveResult res = await client.ReceiveAsync(buffer, CancellationToken.None);
                recv();
                //var str = System.Text.Encoding.Default.GetString(buffer);
                var str = ConvertByteArrayToString(buffer);
                //MessageBox.Show(str);
                dynamic recv_str = JsonConvert.DeserializeObject(str);
                string action = recv_str.action;
               // guess_history.Text += str+'\n';
                if(action== "respond_guess")
                {
                    guess_history.Text+= recv_str.respond_guess + '\n';
                }
                if (action == "recv_message")
                {
                    chat_history.Text += "somebody send:" + recv_str.recv_message + '\n';
                }
                if (action == "creat_room") //ok
                {
                    chat_history.Text += recv_str.creat_room + '\n';
                }
                if (action == "join_room")
                {
                    chat_history.Text += recv_str.join_room + '\n';
                }
            }
            catch
            {
            }
        }

        private void guess_btn_click(object sender, RoutedEventArgs e)
        {
            List<send_format> resend = new List<send_format>()
            {
                new send_format(){action="user_guess",user_guess=guess_input.Text} // json format
             };
            guess_input.Text = "";
            string tosend = JsonConvert.SerializeObject(resend);
            //MessageBox.Show(tosend);
            send(tosend);
        }
      

        private void ws_status_click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show(client.State.ToString());
        }

        private void creat_room_btn_click(object sender, RoutedEventArgs e)
        {
            List<send_format> resend = new List<send_format>()
            {
                new send_format(){action="creat_room"}
             };
            string tosend = JsonConvert.SerializeObject(resend);
            //MessageBox.Show(tosend);
            send(tosend);
        }

        private void join_room_btn_click(object sender, RoutedEventArgs e)
        {
            List<send_format> resend = new List<send_format>()
            {
                new send_format(){action="join_room",join_room=roomid_input.Text}
             };
            roomid_input.Text = "";
            string tosend = JsonConvert.SerializeObject(resend);
            //MessageBox.Show(tosend);
            send(tosend);
        }

        private void chat_send_btn_click(object sender, RoutedEventArgs e)   
        {
            List<send_format> resend = new List<send_format>()
            {
                new send_format(){action="send_message",send_message=chat_input.Text}
             };
            chat_history.Text += "you send: "+chat_input.Text + '\n';
            chat_input.Text = "";

            string tosend = JsonConvert.SerializeObject(resend);
            //MessageBox.Show(tosend);
            send(tosend);
        }
    }
}
