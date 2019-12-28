using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
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
        public MainWindow()
        {
            InitializeComponent();
            init();

        }
        public void init()
        {
            var location = new Uri("ws://192.168.0.105:8001");
            ClientWebSocket client = new ClientWebSocket();
            //Task taskConnect = client.ConnectAsync(location, null);
            //var cts = new CancellationTokenSource();
            //client.ConnectAsync(location, cts.Token);
            client.ConnectAsync(location, CancellationToken.None);
            MessageBox.Show(client.State.ToString());
        }
        private void roomid_btn_click(object sender, RoutedEventArgs e)
        {

        }
        private void guess_btn_click(object sender, RoutedEventArgs e)
        {

        }
    }
}
