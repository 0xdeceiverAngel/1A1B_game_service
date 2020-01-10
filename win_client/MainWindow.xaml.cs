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

namespace _1A1B
{
    /// <summary>
    /// MainWindow.xaml 的互動邏輯
    /// </summary>
    public partial class MainWindow : Window
    {
        ClientWebSocket client = new ClientWebSocket();
        ArraySegment<byte> buffer = new ArraySegment<byte>(new byte[1024]);
        public MainWindow()
        {
            InitializeComponent();
            initAsync();

        }
        public async void  initAsync()
        {
            var location = new Uri("ws://127.0.0.1:9001");

            //Task taskConnect = client.ConnectAsync(location, null);
            //var cts = new CancellationTokenSource();
            //client.ConnectAsync(location, cts.Token);
            await client.ConnectAsync(location, CancellationToken.None);
            recv();
        }
        public void send(string data)
        {
            var encoded = Encoding.UTF8.GetBytes(data);
            var buffer = new ArraySegment<Byte>(encoded, 0, encoded.Length);
            client.SendAsync(buffer, WebSocketMessageType.Text, true, CancellationToken.None);

        }
        private void roomid_btn_click(object sender, RoutedEventArgs e)
        {
            
            
        }
        public string ConvertByteArrayToString(ArraySegment<Byte>data)
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
                WebSocketReceiveResult res = await client.ReceiveAsync(buffer, CancellationToken.None);
                //var str = System.Text.Encoding.Default.GetString(buffer);
                var str = ConvertByteArrayToString(buffer);
                //MessageBox.Show(str);
                chat_history.Text += str;
                recv();
            }
            catch
            {
            }
        }



        private void guess_btn_click(object sender, RoutedEventArgs e)
        {
            string tosend = guess_input.Text;
            guess_input.Text = "";
            send(tosend);
        }
      

        private void ws_status_click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show(client.State.ToString());
        }
    }
}
