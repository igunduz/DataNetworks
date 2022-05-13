/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

// Network topology
//
//       n0---------n1
//
// - Point-to-point link with indicated one-way BW/delay
// - 1 UDP flow from n0 to n1
// - 1 TCP flow from n0 to n1
//

#include <iostream>
#include <fstream>
#include <string>
#include <cassert>

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-helper.h"
#include "ns3/ipv4-global-routing-helper.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("TCP_UDPScript");

int
main (int argc, char *argv[])
{
  std::string delay = "2ms";
  std::string rate = "20Mbps";
  std::string errorModelType = "ns3::RateErrorModel";
  double error_p = 0.025;

  uint32_t PacketSize = 1400;
  float simDuration = 20.0;
  bool tracing = true;

  CommandLine cmd;
  cmd.Parse (argc, argv);

  // Set a few attributes
  Config::SetDefault ("ns3::TcpSocket::SegmentSize", UintegerValue (PacketSize));
  Config::SetDefault ("ns3::RateErrorModel::ErrorRate", DoubleValue (error_p));
  Config::SetDefault ("ns3::RateErrorModel::ErrorUnit", StringValue ("ERROR_UNIT_PACKET"));

  // Explicitly create two nodes.
  NodeContainer nodes;
  nodes.Create (2);

  NodeContainer n0n1 = NodeContainer (nodes.Get(0), nodes.Get(1));

  InternetStackHelper stack;
  stack.Install (nodes);

  // Create chanel between n0 and n1
  PointToPointHelper p2p;
  p2p.SetDeviceAttribute ("DataRate", StringValue (rate));
  p2p.SetChannelAttribute ("Delay", StringValue (delay));

  NetDeviceContainer d0d1 = p2p.Install (n0n1);

  // Add IP addresses.
  Ipv4AddressHelper ipv4;
  ipv4.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer i0i1 = ipv4.Assign (d0d1);

  //Create a UDP flow from node 0 to node 1
  uint16_t port = 8000;
  OnOffHelper onoffudp ("ns3::UdpSocketFactory",
                     Address (InetSocketAddress (i0i1.GetAddress (1), port)));
  onoffudp.SetAttribute ("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
  onoffudp.SetAttribute ("DataRate", StringValue (rate));
  onoffudp.SetAttribute ("PacketSize", UintegerValue (PacketSize));
  ApplicationContainer apps = onoffudp.Install (nodes.Get (0));
  apps.Start (Seconds (1.0));
  apps.Stop (Seconds (10.0));

  // Create a UDP sink on node 1 to receive these packets
  PacketSinkHelper sink ("ns3::UdpSocketFactory",
                         Address (InetSocketAddress (Ipv4Address::GetAny (), port)));
  apps = sink.Install (nodes.Get (1));
  apps.Start (Seconds (1.0));
  apps.Stop (Seconds (10.0));

  //**********************************************************//

  //Create a TCP flow from node 0 to node 1
  uint16_t port2 = 9000;
  OnOffHelper onofftcp ("ns3::TcpSocketFactory",
                     Address (InetSocketAddress (i0i1.GetAddress (1), port2)));
  onofftcp.SetAttribute ("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
  onofftcp.SetAttribute ("DataRate", StringValue (rate));
  onofftcp.SetAttribute ("PacketSize", UintegerValue (PacketSize));
  ApplicationContainer apps2 = onofftcp.Install (nodes.Get (0));
  apps2.Start (Seconds (10.0));
  apps2.Stop (Seconds (simDuration));

  // Create a TCP sink on node 1 to receive these packets
  PacketSinkHelper sink2 ("ns3::TcpSocketFactory",
                         Address (InetSocketAddress (Ipv4Address::GetAny (), port2)));
  apps2 = sink2.Install (nodes.Get (1));
  apps2.Start (Seconds (10.0));
  apps2.Stop (Seconds (simDuration));


  //
  // Error model
  //
  // Create an ErrorModel based on the implementation (constructor)
  // specified by the default TypeId

  ObjectFactory factory;
  factory.SetTypeId (errorModelType);
  Ptr<ErrorModel> em = factory.Create<ErrorModel> ();
  d0d1.Get (1)->SetAttribute ("ReceiveErrorModel", PointerValue (em));

  if (tracing)
    {
      AsciiTraceHelper ascii;
      p2p.EnableAsciiAll (ascii.CreateFileStream ("udp_tcp.tr"));
      p2p.EnablePcapAll ("udp_tcp", true);
    }

  Simulator::Stop (Seconds (simDuration));
  Simulator::Run ();
  Simulator::Destroy ();
  return 0;
}
