"""
Curriculum Data Generator for Cybersecurity Trainer Task Manager.

Generates the complete 196-day master curriculum adhering to Section 8 of
the Software Development Requirements specification.

Outputs:
- backend/app/db/seeds/curriculum_data.json (Used by DB seeder)
- curriculum/roadmap.json
- curriculum/daily_tasks.json
"""

import json
from pathlib import Path

# Complete 28-Week (196 Days) Curriculum Definition
WEEKS_DATA = [
    # ── Phase 1: Computer Foundations & Networking (Weeks 1–6) ─────────────
    {
        "phase": "Phase 1: Foundations & Core Systems",
        "phase_order": 1,
        "phase_desc": "Core computer science, operating systems, networking fundamentals, and essential systems administration.",
        "layer": "Computer Foundations",
        "layer_order": 1,
        "layer_desc": "Hardware architecture, CPU, memory, OS processes, syscalls, and low-level computing primitives.",
        "domain": "Computer and OS Foundations",
        "domain_order": 1,
        "days": [
            {
                "day": 1,
                "name": "CPU, RAM, storage, kernel, user space",
                "desc": "Understand core hardware architecture, memory hierarchies, CPU execution cycle, and the distinction between kernel and user space.",
                "difficulty": "beginner",
                "hours": 3.0,
                "objectives": [
                    "Explain the fetch-decode-execute cycle and register functions.",
                    "Differentiate between L1/L2/L3 cache, volatile RAM, and persistent storage.",
                    "Describe the boundary and protection rings between user space and kernel space."
                ]
            },
            {
                "day": 2,
                "name": "Processes and process lifecycle",
                "desc": "Study how operating systems spawn, schedule, and terminate processes, including PCB structure and state transitions.",
                "difficulty": "beginner",
                "hours": 3.0,
                "objectives": [
                    "Diagram the process state lifecycle (Ready, Running, Blocked, Terminated).",
                    "Inspect running processes and process IDs on the system.",
                    "Explain the fork-exec pattern and orphan/zombie process mechanics."
                ]
            },
            {
                "day": 3,
                "name": "Threads and concurrency basics",
                "desc": "Explore multithreading, shared memory spaces, race conditions, and synchronization primitives.",
                "difficulty": "beginner",
                "hours": 3.0,
                "objectives": [
                    "Distinguish between processes and threads regarding memory and execution context.",
                    "Identify common concurrency issues such as race conditions and deadlocks.",
                    "Explain mutexes, semaphores, and thread safety principles."
                ]
            },
            {
                "day": 4,
                "name": "System calls and privilege boundary",
                "desc": "Examine how user programs request kernel services via software interrupts and syscall tables.",
                "difficulty": "intermediate",
                "hours": 3.5,
                "objectives": [
                    "Map how a standard library call transitions to a CPU syscall trap.",
                    "Trace common syscalls (read, write, open, mmap) using system tracing tools.",
                    "Explain the security significance of the syscall privilege boundary."
                ]
            },
            {
                "day": 5,
                "name": "Filesystems and file descriptors",
                "desc": "Analyze storage abstractions, inode structures, virtual filesystems, and standard input/output descriptors.",
                "difficulty": "beginner",
                "hours": 3.0,
                "objectives": [
                    "Explain inodes, hard links, symbolic links, and directory table structures.",
                    "Trace file descriptor allocation for standard streams (stdin, stdout, stderr).",
                    "Demonstrate file redirection and pipeline chaining."
                ]
            },
            {
                "day": 6,
                "name": "Network interfaces and sockets",
                "desc": "Learn how the OS represents network hardware and provides network communication endpoints via the Berkeley sockets API.",
                "difficulty": "intermediate",
                "hours": 3.5,
                "objectives": [
                    "Explain socket creation, binding, listening, and connection establishment primitives.",
                    "Inspect network interfaces, MTU, and hardware link statuses.",
                    "Trace socket lifecycle states using system tools."
                ]
            },
            {
                "day": 7,
                "name": "Explain the complete program-to-packet chain",
                "desc": "Synthesize the entire journey from application execution down through syscalls, sockets, OS network stack, to physical packet transmission.",
                "difficulty": "intermediate",
                "hours": 4.0,
                "objectives": [
                    "Draw and document the complete path: program -> process -> syscall -> socket -> packet -> interface -> network.",
                    "Explain the kernel-space buffer transitions and NIC interrupt handling.",
                    "Teach the program-to-packet chain aloud from first principles."
                ]
            }
        ]
    },
    {
        "phase": "Phase 1: Foundations & Core Systems",
        "phase_order": 1,
        "phase_desc": "Core computer science, operating systems, networking fundamentals, and essential systems administration.",
        "layer": "Networking",
        "layer_order": 2,
        "layer_desc": "Computer networking, OSI and TCP/IP models, routing, switching, core services, and network diagnostics.",
        "domain": "OSI/TCP-IP and Ethernet",
        "domain_order": 1,
        "days": [
            {
                "day": 8,
                "name": "OSI model and why layers exist",
                "desc": "Study the 7-layer Open Systems Interconnection reference model and the rationale for modular protocol encapsulation.",
                "difficulty": "beginner",
                "hours": 3.0,
                "objectives": [
                    "List all 7 layers of the OSI model and their primary responsibilities.",
                    "Explain protocol data units (PDUs) and encapsulation/decapsulation across layers.",
                    "Identify at least two real-world protocols associated with each layer."
                ]
            },
            {
                "day": 9,
                "name": "TCP/IP model",
                "desc": "Analyze the practical 4-layer DoD/Internet model and compare its architectural boundaries against the theoretical OSI stack.",
                "difficulty": "beginner",
                "hours": 3.0,
                "objectives": [
                    "Map TCP/IP layers (Network Access, Internet, Transport, Application) to OSI layers.",
                    "Describe how headers and trailers are appended during packet traversal.",
                    "Analyze standard packet captures to visually verify header nesting."
                ]
            },
            {
                "day": 10,
                "name": "Ethernet frames",
                "desc": "Inspect Layer 2 framing, preamble, payload limits, EtherType fields, and Frame Check Sequence (FCS) error detection.",
                "difficulty": "beginner",
                "hours": 3.0,
                "objectives": [
                    "Break down the fields of an IEEE 802.3 and Ethernet II frame.",
                    "Explain maximum transmission unit (MTU) limits and jumbo frames.",
                    "Verify frame structure using packet capture analysis."
                ]
            },
            {
                "day": 11,
                "name": "MAC addressing",
                "desc": "Understand 48-bit physical addressing, Organizationally Unique Identifiers (OUI), unicast, broadcast, and multicast MACs.",
                "difficulty": "beginner",
                "hours": 2.5,
                "objectives": [
                    "Parse OUI and device-specific octets in standard MAC addresses.",
                    "Differentiate between unicast, broadcast (FF:FF:FF:FF:FF:FF), and multicast MAC schemes.",
                    "Inspect local switch-port MAC address learning behavior in a lab."
                ]
            },
            {
                "day": 12,
                "name": "ARP fundamentals",
                "desc": "Investigate Address Resolution Protocol: resolving 32-bit IP addresses to 48-bit hardware MAC addresses on local broadcast domains.",
                "difficulty": "beginner",
                "hours": 3.0,
                "objectives": [
                    "Diagram the ARP Request broadcast and ARP Reply unicast sequence.",
                    "Inspect the operating system's local ARP cache table.",
                    "Explain the fundamental trust assumption of ARP and why it lacks authentication."
                ]
            },
            {
                "day": 13,
                "name": "Inspect ARP with Wireshark",
                "desc": "Capture and analyze live ARP traffic in an isolated test network to observe resolution workflows and gratuitous ARP broadcasts.",
                "difficulty": "intermediate",
                "hours": 3.5,
                "objectives": [
                    "Set up an isolated Wireshark capture filter for ARP traffic (`arp`).",
                    "Analyze opcode 1 (request) and opcode 2 (reply) packet structures.",
                    "Record defensive observations regarding ARP broadcast visibility."
                ]
            },
            {
                "day": 14,
                "name": "Weekly lab + teach Ethernet/ARP from first principles",
                "desc": "Consolidate Week 2 learnings by executing an end-to-end local networking lab and delivering a structured lesson on Ethernet and ARP.",
                "difficulty": "intermediate",
                "hours": 4.0,
                "objectives": [
                    "Build a multi-host isolated network and trace end-to-end frame delivery.",
                    "Create a visual diagram explaining MAC learning and ARP resolution.",
                    "Deliver an explanation of Layer 2 communications suitable for a junior learner."
                ]
            }
        ]
    },
    {
        "phase": "Phase 1: Foundations & Core Systems",
        "phase_order": 1,
        "phase_desc": "Core computer science, operating systems, networking fundamentals, and essential systems administration.",
        "layer": "Networking",
        "layer_order": 2,
        "layer_desc": "Computer networking, OSI and TCP/IP models, routing, switching, core services, and network diagnostics.",
        "domain": "IP Addressing and Routing",
        "domain_order": 2,
        "days": [
            {
                "day": 15,
                "name": "IPv4",
                "desc": "Study the IPv4 header structure, 32-bit addressing, TTL mechanics, fragmentation flags, and private vs public address blocks (RFC 1918).",
                "difficulty": "beginner",
                "hours": 3.0,
                "objectives": [
                    "Deconstruct all fields of the IPv4 packet header.",
                    "Identify Class A, B, and C private IPv4 address allocations.",
                    "Explain TTL decrementing and packet expiration."
                ]
            },
            {
                "day": 16,
                "name": "Subnet masks",
                "desc": "Understand how subnet masks partition an IP address into distinct network and host portions using bitwise AND operations.",
                "difficulty": "beginner",
                "hours": 3.0,
                "objectives": [
                    "Convert dotted-decimal subnet masks to binary representation.",
                    "Perform bitwise AND calculation to determine the network ID from an IP and mask.",
                    "Calculate total available host addresses for standard subnet masks."
                ]
            },
            {
                "day": 17,
                "name": "CIDR",
                "desc": "Master Classless Inter-Domain Routing prefix notation, variable-length subnet masking (VLSM), and route aggregation.",
                "difficulty": "intermediate",
                "hours": 3.5,
                "objectives": [
                    "Convert between CIDR prefix notation (/24, /27, /30) and dotted-decimal masks.",
                    "Determine subnet size, usable host range, and broadcast address given a CIDR block.",
                    "Calculate supernetting and route summarization prefixes."
                ]
            },
            {
                "day": 18,
                "name": "Subnetting practice",
                "desc": "Intensive hands-on calculation drills: design custom subnetting plans for complex enterprise network requirements.",
                "difficulty": "intermediate",
                "hours": 4.0,
                "objectives": [
                    "Design a subnet hierarchy for 4 departmental networks of varying host counts.",
                    "Calculate network boundaries, usable IP ranges, and broadcast IPs with zero error.",
                    "Verify calculations using IP subnet calculator verification tools."
                ]
            },
            {
                "day": 19,
                "name": "IPv6 fundamentals",
                "desc": "Explore 128-bit IPv6 addressing architecture, hexadecimal notation, compression rules, and neighbor discovery protocol (NDP).",
                "difficulty": "intermediate",
                "hours": 3.5,
                "objectives": [
                    "Format and compress IPv6 addresses correctly following RFC 5952.",
                    "Differentiate between link-local (fe80::), global unicast (2000::), and unique local addresses.",
                    "Compare IPv6 Neighbor Discovery Protocol (NDP) against IPv4 ARP."
                ]
            },
            {
                "day": 20,
                "name": "Routing fundamentals",
                "desc": "Investigate routing tables, default gateways, static routes, longest-prefix matching, and dynamic routing protocol concepts.",
                "difficulty": "intermediate",
                "hours": 3.5,
                "objectives": [
                    "Inspect and interpret the host routing table (`ip route` or `route print`).",
                    "Explain the concept and necessity of the Default Gateway.",
                    "Demonstrate how longest prefix matching selects packet forward paths."
                ]
            },
            {
                "day": 21,
                "name": "Packet-path troubleshooting exercise",
                "desc": "Execute an integrated lab to troubleshoot routing anomalies, black holes, and misconfigured gateways across multiple subnets.",
                "difficulty": "intermediate",
                "hours": 4.0,
                "objectives": [
                    "Trace and diagnose packet drops across a simulated 3-router topology.",
                    "Use ping and traceroute to isolate the exact point of packet failure.",
                    "Write a root-cause remediation report for the simulated outage."
                ]
            }
        ]
    },
    {
        "phase": "Phase 1: Foundations & Core Systems",
        "phase_order": 1,
        "phase_desc": "Core computer science, operating systems, networking fundamentals, and essential systems administration.",
        "layer": "Networking",
        "layer_order": 2,
        "layer_desc": "Computer networking, OSI and TCP/IP models, routing, switching, core services, and network diagnostics.",
        "domain": "Core Network Services",
        "domain_order": 3,
        "days": [
            {
                "day": 22,
                "name": "DHCP",
                "desc": "Analyze Dynamic Host Configuration Protocol: Discover, Offer, Request, Acknowledge (DORA) lifecycle and lease renewals.",
                "difficulty": "beginner",
                "hours": 3.0,
                "objectives": [
                    "Trace the 4-step DHCP DORA sequence with packet capture analysis.",
                    "Identify DHCP options: gateway, DNS servers, lease duration.",
                    "Explain DHCP starvation and rogue DHCP server security risks."
                ]
            },
            {
                "day": 23,
                "name": "DNS",
                "desc": "Deconstruct the Domain Name System hierarchy: root servers, TLDs, authoritative nameservers, recursion, and common record types.",
                "difficulty": "intermediate",
                "hours": 3.5,
                "objectives": [
                    "Explain recursive vs iterative DNS resolution workflows.",
                    "Differentiate between A, AAAA, CNAME, MX, TXT, and PTR records.",
                    "Use `dig` and `nslookup` to perform manual DNS queries and zone checks."
                ]
            },
            {
                "day": 24,
                "name": "ICMP",
                "desc": "Study Internet Control Message Protocol: error reporting, echo requests/replies, unreachable types, and MTU discovery.",
                "difficulty": "beginner",
                "hours": 3.0,
                "objectives": [
                    "Identify ICMP Type 0 (Echo Reply), Type 8 (Echo Request), and Type 3 (Destination Unreachable).",
                    "Explain how `traceroute` leverages TTL expiration and ICMP Time Exceeded (Type 11).",
                    "Analyze ICMP tunneling and network reconnaissance implications."
                ]
            },
            {
                "day": 25,
                "name": "TCP",
                "desc": "Examine Transmission Control Protocol: reliable streams, sequence/acknowledgment numbers, windowing, and the 3-way handshake.",
                "difficulty": "intermediate",
                "hours": 4.0,
                "objectives": [
                    "Diagram the SYN, SYN-ACK, ACK connection establishment sequence.",
                    "Explain TCP flags: SYN, ACK, FIN, RST, PSH, URG.",
                    "Analyze TCP sliding window flow control and congestion avoidance."
                ]
            },
            {
                "day": 26,
                "name": "UDP",
                "desc": "Analyze User Datagram Protocol: connectionless, lightweight, low-overhead transmission, and suitable use cases.",
                "difficulty": "beginner",
                "hours": 2.5,
                "objectives": [
                    "Contrast UDP 8-byte header overhead against TCP header complexity.",
                    "Identify services relying on UDP (DNS, DHCP, VoIP, streaming) and explain why.",
                    "Discuss UDP amplification and spoofing vectors."
                ]
            },
            {
                "day": 27,
                "name": "Ports and sockets",
                "desc": "Understand 16-bit transport layer port addressing, well-known ports (0-1023), registered ports, and ephemeral client ports.",
                "difficulty": "beginner",
                "hours": 3.0,
                "objectives": [
                    "Memorize essential well-known service ports (21, 22, 25, 53, 80, 110, 443, 445, 3389).",
                    "Explain client ephemeral port selection for socket pair uniqueness.",
                    "Use `ss` and `netstat` to map local listening services to sockets."
                ]
            },
            {
                "day": 28,
                "name": "Compare TCP vs UDP by capturing real traffic in a lab",
                "desc": "Hands-on capture lab: contrast TCP stateful handshakes/teardowns against UDP packet streams using Wireshark.",
                "difficulty": "intermediate",
                "hours": 4.0,
                "objectives": [
                    "Capture HTTP (TCP) and DNS (UDP) transactions simultaneously.",
                    "Compare latency, packet count, and retransmission behavior.",
                    "Document the trade-offs between reliability and performance."
                ]
            }
        ]
    },
    {
        "phase": "Phase 1: Foundations & Core Systems",
        "phase_order": 1,
        "phase_desc": "Core computer science, operating systems, networking fundamentals, and essential systems administration.",
        "layer": "Networking",
        "layer_order": 2,
        "layer_desc": "Computer networking, OSI and TCP/IP models, routing, switching, core services, and network diagnostics.",
        "domain": "Network Security and Tools",
        "domain_order": 4,
        "days": [
            {
                "day": 29,
                "name": "NAT",
                "desc": "Explore Network Address Translation: Source NAT, Destination NAT/Port Forwarding, and PAT/NAT Overload.",
                "difficulty": "intermediate",
                "hours": 3.5,
                "objectives": [
                    "Explain how Port Address Translation multiplexes private IP pools over a single public IP.",
                    "Inspect translation state tables on a router or firewall.",
                    "Analyze NAT's dual impact on IPv4 address exhaustion and inbound security boundaries."
                ]
            },
            {
                "day": 30,
                "name": "Firewalls",
                "desc": "Study packet filtering, stateful inspection, application-layer firewalls, and default-deny security policies.",
                "difficulty": "intermediate",
                "hours": 3.5,
                "objectives": [
                    "Differentiate between stateless packet filters and stateful connection tracking firewalls.",
                    "Write fundamental ingress and egress rules enforcing least privilege.",
                    "Test firewall drop vs reject responses with network scanners."
                ]
            },
            {
                "day": 31,
                "name": "Network segmentation",
                "desc": "Investigate physical vs logical isolation, VLANs (802.1Q), DMZs, zero-trust microsegmentation, and jump boxes.",
                "difficulty": "intermediate",
                "hours": 3.5,
                "objectives": [
                    "Explain 802.1Q VLAN tagging and trunk port configuration.",
                    "Design a segmented architecture isolating management, server, and client networks.",
                    "Evaluate lateral movement restriction achieved by segmentation."
                ]
            },
            {
                "day": 32,
                "name": "IDS/IPS",
                "desc": "Examine Intrusion Detection and Prevention Systems: signature-based vs anomaly-based detection, inline vs passive deployment.",
                "difficulty": "intermediate",
                "hours": 3.5,
                "objectives": [
                    "Contrast passive SPAN/TAP IDS monitoring against inline active IPS blocking.",
                    "Explain signature pattern matching and false positive/negative trade-offs.",
                    "Review sample Snort/Suricata detection rules."
                ]
            },
            {
                "day": 33,
                "name": "VPNs and proxies",
                "desc": "Study secure tunneling protocols (IPsec, OpenVPN, WireGuard), forward proxies, reverse proxies, and traffic encapsulation.",
                "difficulty": "intermediate",
                "hours": 3.5,
                "objectives": [
                    "Compare site-to-site and remote-access VPN architectures.",
                    "Analyze IPsec ESP mode encryption and authentication headers.",
                    "Explain reverse proxy load balancing and TLS termination."
                ]
            },
            {
                "day": 34,
                "name": "Traffic analysis",
                "desc": "Methods for monitoring network flows, statistical bandwidth baselining, top talkers identification, and anomalous traffic detection.",
                "difficulty": "intermediate",
                "hours": 4.0,
                "objectives": [
                    "Analyze NetFlow/IPFIX flow statistics to detect high-volume data exfiltration.",
                    "Identify unencrypted protocol leakage in baseline captures.",
                    "Create a Wireshark IO graph to locate transmission spikes."
                ]
            },
            {
                "day": 35,
                "name": "Build a network-security troubleshooting lab",
                "desc": "Capstone lab for Network Security: configure segmented subnets, apply firewall policies, and verify communication boundaries.",
                "difficulty": "advanced",
                "hours": 4.5,
                "objectives": [
                    "Implement a 3-subnet architecture with DMZ in a virtualized lab.",
                    "Configure firewall rules blocking client-to-management direct access.",
                    "Verify rule enforcement using scanning and audit logging."
                ]
            },
            {
                "day": 36,
                "name": "Nmap fundamentals",
                "desc": "Master Network Mapper architecture: host discovery techniques, scan types (-sT, -sS, -sU), and timing templates.",
                "difficulty": "intermediate",
                "hours": 3.5,
                "objectives": [
                    "Explain the difference between TCP Connect (-sT) and SYN Stealth (-sS) scans.",
                    "Select appropriate scan timing templates (-T0 through -T5) for specific network conditions.",
                    "Interpret Nmap open, closed, and filtered port status outputs."
                ]
            },
            {
                "day": 37,
                "name": "Nmap host discovery in an authorized lab",
                "desc": "Conduct systematic network sweep discovery using ICMP, TCP SYN ping, UDP ping, and ARP requests.",
                "difficulty": "intermediate",
                "hours": 3.5,
                "objectives": [
                    "Perform ARP ping discovery across a local CIDR subnet (-PR).",
                    "Conduct TCP SYN ping sweeps on remote subnets (-PS).",
                    "Document all active IP addresses and identify rogue test hosts."
                ]
            },
            {
                "day": 38,
                "name": "Service/version enumeration",
                "desc": "Probe open ports for service banners, application versions (-sV), and OS fingerprinting (-O).",
                "difficulty": "intermediate",
                "hours": 4.0,
                "objectives": [
                    "Run version detection and analyze banner grabbing mechanics.",
                    "Explain OS fingerprinting through TCP/IP stack behavior differences.",
                    "Map identified service versions against known CVE repositories."
                ]
            },
            {
                "day": 39,
                "name": "Wireshark workflows",
                "desc": "Advanced packet analysis: display filters, follow TCP streams, protocol hierarchy statistics, and expert info diagnostics.",
                "difficulty": "intermediate",
                "hours": 3.5,
                "objectives": [
                    "Write complex Wireshark display filters combining logic operators.",
                    "Reconstruct full application-layer conversations using Follow Stream.",
                    "Triage network anomalies using the Wireshark Expert Information pane."
                ]
            },
            {
                "day": 40,
                "name": "tcpdump",
                "desc": "Master command-line packet capturing: Berkeley Packet Filters (BPF), output formatting, and PCAP file rotation.",
                "difficulty": "intermediate",
                "hours": 3.5,
                "objectives": [
                    "Capture live traffic with specific BPF filters (e.g. `port 80 and not host 10.0.0.1`).",
                    "Save and read capture files with `-w` and `-r` flags without truncating packets.",
                    "Inspect packet payloads in ASCII and hex directly in the terminal."
                ]
            },
            {
                "day": 41,
                "name": "ss, dig, traceroute/mtr",
                "desc": "Command-line toolkit proficiency: socket statistics (`ss`), DNS exploration (`dig`), and continuous path diagnostics (`mtr`).",
                "difficulty": "intermediate",
                "hours": 3.0,
                "objectives": [
                    "Use `ss -tulnp` to identify listening services and associated process PIDs.",
                    "Execute authoritative DNS queries with `dig +trace` to observe delegation.",
                    "Use `mtr` to locate packet loss and jitter across WAN hops."
                ]
            },
            {
                "day": 42,
                "name": "Netcat + integrated network investigation lab",
                "desc": "The Swiss Army knife of networking: client/server connections, port listening, banner grabbing, and raw data transmission.",
                "difficulty": "intermediate",
                "hours": 4.5,
                "objectives": [
                    "Set up arbitrary TCP/UDP listeners and test port reachability with `nc`.",
                    "Perform manual HTTP, SMTP, and FTP protocol interactions over Netcat.",
                    "Complete an integrated network diagnostic assessment combining nmap, tcpdump, and nc."
                ]
            }
        ]
    }
]

# We will generate all 28 weeks programmatically using structured domain templates
# covering the exact roadmap in Section 8!

def get_all_196_days():
    """Build the master 196-day curriculum matching Section 8."""
    
    # 28 Weeks structure definitions
    weeks_blueprint = [
        # (Week Num, Phase Name, Phase Order, Layer Name, Layer Order, Domain Name, [7 Day Titles and Focus])
        (1, "Phase 1: Foundations & Core Systems", 1, "Computer Foundations", 1, "Computer and OS Foundations", [
            ("CPU, RAM, storage, kernel, user space", "Hardware, memory, execution cycle, and protection rings.", "beginner", 3.0),
            ("processes and process lifecycle", "Process creation, states, scheduling, and lifecycle management.", "beginner", 3.0),
            ("threads and concurrency basics", "Multithreading, shared memory, race conditions, and synchronization.", "beginner", 3.0),
            ("system calls and privilege boundary", "Kernel privilege boundary, syscall transitions, and strace introduction.", "intermediate", 3.5),
            ("filesystems and file descriptors", "Inodes, file system hierarchy, file descriptors, and stream redirection.", "beginner", 3.0),
            ("network interfaces and sockets", "Network adapters, socket API, and kernel network endpoint representations.", "intermediate", 3.5),
            ("explain the complete program-to-packet chain", "Comprehensive synthesis of program -> syscall -> socket -> packet flow.", "intermediate", 4.0),
        ]),
        (2, "Phase 1: Foundations & Core Systems", 1, "Networking", 2, "OSI and Ethernet", [
            ("OSI model and why layers exist", "7-layer reference model, protocol encapsulation, and abstraction boundaries.", "beginner", 3.0),
            ("TCP/IP model", "4-layer DoD internet model and packet header decapsulation.", "beginner", 3.0),
            ("Ethernet frames", "Data link layer framing, preamble, MTU, and frame check sequence.", "beginner", 3.0),
            ("MAC addressing", "48-bit hardware addresses, OUI parsing, and unicast/multicast/broadcast MACs.", "beginner", 2.5),
            ("ARP fundamentals", "Address Resolution Protocol request/reply cycle and local cache table.", "beginner", 3.0),
            ("inspect ARP with Wireshark", "Packet capture analysis of live ARP transactions and gratuitous ARP.", "intermediate", 3.5),
            ("weekly lab + teach Ethernet/ARP from first principles", "Consolidated lab exercise and structured teaching presentation on Layer 2.", "intermediate", 4.0),
        ]),
        (3, "Phase 1: Foundations & Core Systems", 1, "Networking", 2, "IP Addressing and Routing", [
            ("IPv4", "32-bit addressing, packet headers, TTL mechanics, and private address blocks.", "beginner", 3.0),
            ("subnet masks", "Bitwise AND operations, network IDs, and host calculation formulas.", "beginner", 3.0),
            ("CIDR", "Classless Inter-Domain Routing prefix notation and route summarization.", "intermediate", 3.5),
            ("subnetting practice", "Calculation drills and enterprise VLSM subnetting design challenges.", "intermediate", 4.0),
            ("IPv6 fundamentals", "128-bit address syntax, compression rules, and Neighbor Discovery Protocol.", "intermediate", 3.5),
            ("routing fundamentals", "Routing tables, default gateways, static routes, and longest-prefix matching.", "intermediate", 3.5),
            ("packet-path troubleshooting exercise", "Diagnosing multi-subnet routing failures and gateway misconfigurations.", "intermediate", 4.0),
        ]),
        (4, "Phase 1: Foundations & Core Systems", 1, "Networking", 2, "Core Network Services", [
            ("DHCP", "DORA lifecycle, lease management, option fields, and rogue server security risks.", "beginner", 3.0),
            ("DNS", "Hierarchical resolution, root servers, recursive queries, and resource record types.", "intermediate", 3.5),
            ("ICMP", "Internet Control Message Protocol error signaling, echo requests, and path MTU.", "beginner", 3.0),
            ("TCP", "Connection-oriented streams, 3-way handshake, flags, sequence numbers, and windowing.", "intermediate", 4.0),
            ("UDP", "Connectionless datagram transport, low-latency protocols, and amplification threats.", "beginner", 2.5),
            ("ports and sockets", "16-bit transport ports, well-known port mapping, and socket pair identification.", "beginner", 3.0),
            ("compare TCP vs UDP by capturing real traffic in a lab", "Side-by-side traffic capture and latency/overhead comparison in Wireshark.", "intermediate", 4.0),
        ]),
        (5, "Phase 1: Foundations & Core Systems", 1, "Networking", 2, "Network Security", [
            ("NAT", "Source NAT, Destination NAT/Port forwarding, and PAT overload mechanics.", "intermediate", 3.5),
            ("firewalls", "Stateless packet filtering vs stateful inspection and default-deny policies.", "intermediate", 3.5),
            ("network segmentation", "Logical network isolation, 802.1Q VLANs, DMZs, and jump box architectures.", "intermediate", 3.5),
            ("IDS/IPS", "Intrusion detection/prevention architectures, signature vs anomaly models, and inline taps.", "intermediate", 3.5),
            ("VPNs and proxies", "Tunneling protocols (IPsec, WireGuard), forward proxies, and reverse proxy termination.", "intermediate", 3.5),
            ("traffic analysis", "Flow monitoring, statistical baselining, anomaly identification, and IO graphs.", "intermediate", 4.0),
            ("build a network-security troubleshooting lab", "Hands-on capstone lab: multi-zone firewall configuration and segmentation testing.", "advanced", 4.5),
        ]),
        (6, "Phase 1: Foundations & Core Systems", 1, "Networking", 2, "Network Tools", [
            ("Nmap fundamentals", "Network mapping principles, timing templates, and TCP connect vs SYN scan options.", "intermediate", 3.5),
            ("Nmap host discovery in an authorized lab", "Conducting host discovery sweeps using ARP, ICMP, and TCP ping vectors.", "intermediate", 3.5),
            ("service/version enumeration", "Banner grabbing, service fingerprinting, and OS detection workflows.", "intermediate", 4.0),
            ("Wireshark workflows", "Advanced display filter syntax, TCP stream following, and protocol hierarchy stats.", "intermediate", 3.5),
            ("tcpdump", "CLI packet capture filtering, BPF syntax, and PCAP inspection.", "intermediate", 3.5),
            ("ss, dig, traceroute/mtr", "Linux networking diagnostics: socket inspection, recursive DNS tracing, and route mtr.", "intermediate", 3.0),
            ("Netcat + integrated network investigation lab", "Arbitrary TCP/UDP connections, banner interaction, and comprehensive diagnostic challenge.", "intermediate", 4.5),
        ]),
        (7, "Phase 1: Foundations & Core Systems", 1, "Linux", 3, "Linux Fundamentals", [
            ("Linux architecture", "Kernel, shell, GNU utilities, user space separation, and boot sequence overview.", "beginner", 3.0),
            ("filesystem hierarchy", "Linux Filesystem Hierarchy Standard (FHS): /etc, /var, /bin, /home, /dev, /tmp.", "beginner", 3.0),
            ("users and groups", "User accounts, /etc/passwd, /etc/shadow, /etc/group, and UID/GID management.", "beginner", 3.0),
            ("permissions", "Read, write, execute bits, octal and symbolic modes, and umask calculation.", "beginner", 3.0),
            ("chmod/chown", "Modifying ownership and permissions, SUID, SGID, and sticky bit implementation.", "intermediate", 3.5),
            ("processes and ps", "Process tree inspection (`ps`, `pstree`, `top`), signals, and background jobs.", "beginner", 3.0),
            ("Linux troubleshooting assessment", "Hands-on troubleshooting: resolve broken permissions, missing groups, and orphaned processes.", "intermediate", 4.0),
        ]),
        (8, "Phase 1: Foundations & Core Systems", 1, "Linux", 3, "Linux Administration", [
            ("services and systemd", "Systemd initialization system, unit files, targets, and daemon architecture.", "intermediate", 3.5),
            ("systemctl", "Managing service lifecycles (start, stop, enable, disable, status, mask).", "intermediate", 3.0),
            ("journalctl and logs", "Querying systemd journal logs, /var/log analysis, priority filtering, and log rotation.", "intermediate", 3.5),
            ("SSH", "Secure Shell server configuration, key pair generation, authorized_keys, and agent forwarding.", "intermediate", 3.5),
            ("cron", "Scheduled tasks with crontab, system cron directories, and syntax troubleshooting.", "beginner", 3.0),
            ("environment variables and shell", "PATH evaluation, export variables, shell configuration files (.bashrc, /etc/profile).", "beginner", 3.0),
            ("shell scripting mini-project", "Write an automated system health check and log backup bash script.", "intermediate", 4.5),
        ]),
        (9, "Phase 1: Foundations & Core Systems", 1, "Linux", 3, "Linux Internals", [
            ("package management", "Debian (apt) and RedHat (dnf/rpm) package managers, repositories, and dependency trees.", "intermediate", 3.0),
            ("/proc", "Virtual filesystem representing kernel state, hardware devices, and per-PID process metrics.", "intermediate", 3.5),
            ("/sys", "Kernel device model, driver parameters, subsystem configuration, and sysfs exploration.", "intermediate", 3.5),
            ("capabilities", "Privilege splitting with Linux capabilities (CAP_NET_BIND_SERVICE, CAP_SYS_ADMIN).", "advanced", 4.0),
            ("namespaces", "Isolation primitives (PID, NET, MNT, IPC, UTS) forming containerization foundations.", "advanced", 4.0),
            ("strace", "Intercepting and recording system calls invoked by binaries during execution.", "advanced", 4.0),
            ("troubleshoot a deliberately broken Linux service", "Diagnose and repair a damaged web server service using system logs and strace.", "advanced", 4.5),
        ]),
        (10, "Phase 1: Foundations & Core Systems", 1, "Linux", 3, "Linux Security", [
            ("Linux authentication", "Pluggable Authentication Modules (PAM), /etc/pam.d/ configurations, and shadow security.", "intermediate", 3.5),
            ("SSH hardening concepts", "Disabling root login, enforcing key authentication, port changing, and fail2ban integration.", "intermediate", 3.5),
            ("permissions and privilege boundaries", "Evaluating sudoers configuration, wheel group, and sudo command restrictions.", "intermediate", 3.5),
            ("service exposure", "Auditing network listening ports and bounding services to local loopback addresses.", "intermediate", 3.0),
            ("logs and indicators", "Parsing auth.log and secure logs for brute-force attempts and anomalous logins.", "intermediate", 3.5),
            ("Linux attack surface mapping", "Comprehensive enumeration of installed packages, SUID binaries, and writable paths.", "intermediate", 4.0),
            ("teach Linux security to a beginner", "Deliver a structured pedagogical walkthrough of Linux security hardening.", "intermediate", 4.0),
        ]),
        (11, "Phase 1: Foundations & Core Systems", 1, "Windows", 4, "Windows Foundations", [
            ("Windows architecture", "User mode, kernel mode, HAL, executive subsystems, and Win32 API structure.", "intermediate", 3.5),
            ("processes", "Windows processes, threads, handles, DLL loading, and token models.", "intermediate", 3.5),
            ("services", "Service Control Manager (SCM), service accounts (SYSTEM, Network Service), and startup types.", "intermediate", 3.0),
            ("Registry", "HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER, hive structure, and registry navigation.", "intermediate", 3.5),
            ("Event Viewer", "Windows event log architecture (Application, Security, System) and Event ID semantics.", "intermediate", 3.5),
            ("PowerShell", "Commandlets, object-oriented pipelines, scripting basics, and system administration queries.", "intermediate", 4.0),
            ("Windows troubleshooting assessment", "Hands-on diagnostic scenario: resolve corrupted registry keys and failing services.", "intermediate", 4.0),
        ]),
        (12, "Phase 1: Foundations & Core Systems", 1, "Windows", 4, "Windows Security", [
            ("NTFS permissions", "NTFS file system security, standard and special permissions, and inheritance rules.", "intermediate", 3.5),
            ("ACLs", "Discretionary Access Control Lists (DACLs) vs System Access Control Lists (SACLs).", "intermediate", 3.5),
            ("Windows authentication", "Security Support Provider Interface (SSPI), NTLM challenge-response, and Kerberos overview.", "intermediate", 4.0),
            ("Windows security model", "Security Identifiers (SIDs), access tokens, integrity levels, and User Account Control (UAC).", "intermediate", 4.0),
            ("Windows networking", "SMB/CIFS protocols, Windows Firewall rules, RPC endpoints, and NetBIOS resolution.", "intermediate", 3.5),
            ("Sysinternals", "Tooling mastery: Process Explorer, Process Monitor (Procmon), and Autoruns investigation.", "advanced", 4.5),
            ("Windows security investigation lab", "Investigate a simulated credential exposure and unauthorized persistence in a lab.", "advanced", 4.5),
        ]),

        # ── Phase 2: Security & Exploitation (Weeks 13–20) ───────────────────
        (13, "Phase 2: Security & Exploitation", 2, "Offensive Security", 5, "Penetration-Testing Methodology", [
            ("reconnaissance", "Passive reconnaissance, OSINT techniques, DNS harvesting, and corporate footprinting.", "intermediate", 3.5),
            ("enumeration", "Active network enumeration, service fingerprinting, and account discovery protocols.", "intermediate", 3.5),
            ("attack-surface identification", "Mapping entry points, exposed web portals, unpatched protocols, and trust relationships.", "intermediate", 3.5),
            ("vulnerability discovery", "Correlating version information with CVE databases and automated vulnerability scanners.", "intermediate", 4.0),
            ("validation", "Manual verification of scanner findings to eliminate false positives in isolated labs.", "intermediate", 4.0),
            ("evidence collection and reporting", "Technical note taking, screenshot evidence standards, CVSS scoring, and risk metrics.", "intermediate", 4.0),
            ("produce an end-to-end authorized assessment plan", "Draft a complete Rules of Engagement (RoE) and technical penetration test scope.", "advanced", 4.5),
        ]),
        (14, "Phase 2: Security & Exploitation", 2, "Offensive Security", 5, "Network Penetration Testing", [
            ("SMB", "Server Message Block enumeration, null sessions, share permissions, and common vulnerabilities.", "intermediate", 4.0),
            ("SSH", "SSH configuration audits, weak key exchange algorithms, and credential spray testing.", "intermediate", 3.5),
            ("FTP", "Anonymous FTP access, cleartext credential risks, and directory traversal testing.", "beginner", 3.0),
            ("HTTP service enumeration", "Directory and file brute-forcing, robots.txt inspection, and web technology identification.", "intermediate", 3.5),
            ("DNS enumeration concepts", "Zone transfers (AXFR), sub-domain brute forcing, and reverse lookup records.", "intermediate", 3.5),
            ("common misconfigurations", "Default credentials, unnecessary services, permissive file shares, and wildcard sudo rules.", "intermediate", 4.0),
            ("privilege-escalation fundamentals in an isolated lab", "Identifying local privilege escalation vectors on an authorized test machine.", "advanced", 4.5),
        ]),
        (15, "Phase 2: Security & Exploitation", 2, "Offensive Security", 5, "Exploitation Lifecycle", [
            ("exploitation concepts", "Proof of concept execution, payload staging, shell types (bind vs reverse), and listener setup.", "advanced", 4.0),
            ("post-exploitation concepts", "System situational awareness, credential hunting in memory/files, and sensitive data indexing.", "advanced", 4.0),
            ("persistence concepts", "Scheduled tasks, cron jobs, service creation, and startup registry keys in test systems.", "advanced", 4.0),
            ("lateral movement concepts", "Pivoting, port forwarding, SSH tunneling, and proxychains configuration.", "advanced", 4.5),
            ("evidence handling", "Secure storage of assessment findings, hash integrity verification, and cleanup verification.", "intermediate", 3.5),
            ("remediation mapping", "Translating exploitation vectors into defense-in-depth mitigation roadmaps.", "intermediate", 3.5),
            ("complete a controlled penetration-testing lab and report", "Execute full assessment on an authorized target and author an executive report.", "advanced", 5.0),
        ]),
        (16, "Phase 2: Security & Exploitation", 2, "Web and Application Security", 6, "Web Fundamentals", [
            ("HTTP request/response", "HTTP methods, headers, status codes, keep-alive connections, and raw request parsing.", "beginner", 3.0),
            ("cookies", "Session cookies, flags (HttpOnly, Secure, SameSite), and cookie security implications.", "beginner", 3.0),
            ("sessions", "State management, session identifiers, server-side session stores, and fixation risks.", "intermediate", 3.5),
            ("authentication", "Basic auth, form-based auth, multi-factor authentication, and password storage standards.", "intermediate", 3.5),
            ("authorization", "Role-based access control (RBAC), permission matrices, and privilege enforcement points.", "intermediate", 3.5),
            ("APIs", "REST architecture, endpoints, JSON schemas, API keys, and rate limiting fundamentals.", "intermediate", 3.5),
            ("JWT and token-based authentication", "JSON Web Tokens: header, payload, signature, hashing algorithms, and validation flaws.", "intermediate", 4.0),
        ]),
        (17, "Phase 2: Security & Exploitation", 2, "Web and Application Security", 6, "Web Vulnerabilities I", [
            ("CORS", "Cross-Origin Resource Sharing, preflight OPTIONS requests, origin reflection risks.", "intermediate", 3.5),
            ("SQL injection concepts and safe lab validation", "In-band SQLi, union-based extraction, error-based testing in safe sandboxed databases.", "advanced", 4.5),
            ("XSS", "Cross-Site Scripting: Reflected, Stored, and DOM-based XSS mechanisms and context encoding.", "intermediate", 4.0),
            ("CSRF", "Cross-Site Request Forgery, state-changing requests, anti-CSRF tokens, and SameSite protection.", "intermediate", 3.5),
            ("SSRF", "Server-Side Request Forgery, cloud metadata service probing, and internal network scanning.", "advanced", 4.0),
            ("path traversal", "Directory traversal (dot-dot-slash), arbitrary file disclosure, and path canonicalization.", "intermediate", 3.5),
            ("vulnerable-web-app lab and evidence report", "Hands-on audit of a test application; document technical findings and CVSS scores.", "advanced", 4.5),
        ]),
        (18, "Phase 2: Security & Exploitation", 2, "Web and Application Security", 6, "Web Vulnerabilities II", [
            ("IDOR/BOLA", "Insecure Direct Object References and Broken Object Level Authorization testing.", "intermediate", 3.5),
            ("file-upload vulnerabilities", "Unrestricted file uploads, MIME-type validation bypasses, and executable payloads.", "advanced", 4.0),
            ("command injection concepts", "Executing arbitrary OS commands via vulnerable backend inputs and sanitization bypasses.", "advanced", 4.5),
            ("authentication flaws", "Password reset vulnerabilities, brute-force bypasses, and credential stuffing vectors.", "intermediate", 3.5),
            ("business-logic vulnerabilities", "Circumventing application workflows, shopping cart manipulation, and race conditions.", "intermediate", 4.0),
            ("Burp Suite workflow", "Intercepting proxy, repeater, intruder rate limiting, and target site mapping.", "intermediate", 4.0),
            ("complete an OWASP-style web assessment in an isolated lab", "Full-scale web application penetration test covering OWASP Top 10 vulnerabilities.", "advanced", 5.0),
        ]),
        (19, "Phase 2: Security & Exploitation", 2, "Enterprise Security", 7, "Enterprise Security Foundations", [
            ("Windows domains", "Domain controllers, central identity management, domain trees, and forest architectures.", "intermediate", 3.5),
            ("Active Directory architecture", "AD DS, Schema, global catalog, organizational units (OUs), and replication.", "intermediate", 4.0),
            ("LDAP", "Lightweight Directory Access Protocol, queries, search filters, and directory querying.", "intermediate", 3.5),
            ("Kerberos fundamentals", "Authentication tickets, Key Distribution Center (KDC), AS-REQ, AS-REP, TGS-REQ, TGS-REP.", "advanced", 4.5),
            ("authentication flows", "Step-by-step trace of Kerberos authentication vs NTLM fallbacks.", "advanced", 4.0),
            ("Group Policy", "GPO processing, Group Policy Objects, organizational enforcement, and security templates.", "intermediate", 3.5),
            ("build and document a small authorized AD lab", "Set up a virtualized domain controller and join client workstations for security testing.", "advanced", 5.0),
        ]),
        (20, "Phase 2: Security & Exploitation", 2, "Enterprise Security", 7, "Enterprise Attack and Defense", [
            ("AD attack surface", "Domain enumeration, BloodHound graph analysis concepts, and privileged group auditing.", "advanced", 4.5),
            ("credential concepts", "LSASS memory handling, password hashes, Kerberoasting theory, and AS-REP roasting.", "advanced", 4.5),
            ("lateral movement concepts", "PsExec, WMI/WinRM remote execution, and overpass-the-hash fundamentals.", "advanced", 4.5),
            ("privilege escalation concepts", "Domain escalation vectors, vulnerable GPOs, ACL misconfigurations, and service abuse.", "advanced", 4.5),
            ("enterprise logging", "Windows Event IDs for AD audits (4624, 4625, 4672, 4768, 4769, 4771) and PowerShell script block logging.", "intermediate", 4.0),
            ("detection opportunities", "Identifying abnormal ticket requests, anomalous Kerberos encryption types, and mass enumeration.", "advanced", 4.0),
            ("attack-to-detection exercise", "Execute a controlled Kerberoasting demonstration and analyze the resulting domain event logs.", "advanced", 5.0),
        ]),

        # ── Phase 3: Defensive Security & Analysis (Weeks 21–26) ─────────────
        (21, "Phase 3: Defensive Engineering & Analysis", 3, "SOC and Defensive Security", 8, "SOC Fundamentals", [
            ("SOC purpose and workflow", "Security Operations Center tier roles (Tier 1-3), incident response lifecycles, and SLAs.", "intermediate", 3.5),
            ("logs vs events vs alerts", "Log ingestion volumes, event correlation rules, and alert threshold calibration.", "beginner", 3.0),
            ("Windows Event Logs", "In-depth parsing of security auditing events, Sysmon installation, and telemetry enrichment.", "intermediate", 4.0),
            ("Linux logs", "Analyzing /var/log/auth.log, auditd system audit logs, and web server access logs.", "intermediate", 3.5),
            ("IOC concepts", "Indicators of Compromise: file hashes, IP addresses, domains, and YARA rule basics.", "intermediate", 3.5),
            ("alert triage", "Triaging simulated alerts, determining true vs false positives, and scoping incident impact.", "intermediate", 4.0),
            ("investigate a simulated alert", "End-to-end investigation of a malicious macro phishing alert in a sandbox SIEM.", "advanced", 4.5),
        ]),
        (22, "Phase 3: Defensive Engineering & Analysis", 3, "SOC and Defensive Security", 8, "SIEM and Monitoring", [
            ("SIEM architecture", "Log forwarders, parsers, indexers, storage retention, and correlation engines.", "intermediate", 4.0),
            ("Wazuh", "Open source XDR and SIEM: agent deployment, rule customization, and active response testing.", "intermediate", 4.0),
            ("Elastic", "Elasticsearch, Logstash, Kibana (ELK) stack and Lucene query language fundamentals.", "intermediate", 4.0),
            ("Splunk concepts", "Search Processing Language (SPL), dashboards, indexes, and sourcetype configuration.", "intermediate", 4.0),
            ("network monitoring", "Full packet capture systems, network security monitoring (NSM) architectures.", "intermediate", 3.5),
            ("Zeek", "Bro/Zeek network analysis framework: conn.log, dns.log, and HTTP transaction auditing.", "advanced", 4.5),
            ("Suricata", "Suricata signature rules, fast.log, EVE JSON logging, and alert signature matching.", "advanced", 4.5),
        ]),
        (23, "Phase 3: Defensive Engineering & Analysis", 3, "SOC and Defensive Security", 8, "Detection Engineering", [
            ("attack artifacts", "File modifications, registry keys, process hollowing indicators, and network artifacts.", "advanced", 4.0),
            ("detection logic", "Translating adversary techniques (MITRE ATT&CK) into precise detection rules.", "advanced", 4.5),
            ("investigation workflow", "Evidence preservation, timeline construction, volatile memory capture, and triage.", "advanced", 4.0),
            ("containment", "Host isolation, credential resets, firewall blocking, and malicious process termination.", "intermediate", 3.5),
            ("remediation", "System eradication, persistence cleanup, root-cause closure, and verification scans.", "intermediate", 3.5),
            ("threat intelligence", "Integrating STIX/TAXII threat feeds, MISP platforms, and adversary profiling.", "intermediate", 3.5),
            ("build one complete ATTACK → ARTIFACT → LOG → DETECTION → INVESTIGATION → CONTAINMENT → REMEDIATION case", "Execute full 7-step defensive reasoning case study and publish comprehensive incident writeup.", "expert", 5.5),
        ]),
        (24, "Phase 3: Defensive Engineering & Analysis", 3, "Malware Analysis & Reverse Engineering", 9, "Malware-Analysis Foundations", [
            ("PE files", "Portable Executable structure: DOS header, PE header, optional header, and sections (.text, .data).", "advanced", 4.5),
            ("ELF files", "Executable and Linkable Format structure on Linux: ELF header, program headers, sections.", "advanced", 4.0),
            ("processes and memory", "Virtual memory layouts, stack vs heap allocations, address space layout (ASLR).", "advanced", 4.0),
            ("DLLs/shared libraries", "Dynamic link libraries, import address tables (IAT), export tables, and DLL loading.", "advanced", 4.0),
            ("Windows APIs", "Common Win32 APIs targeted by malware (VirtualAlloc, CreateRemoteThread, WriteProcessMemory).", "advanced", 4.5),
            ("Linux syscalls", "Malware interactions with ptrace, mprotect, fork, and network socket syscalls.", "advanced", 4.0),
            ("hashes, strings, and metadata", "Cryptographic hashes (MD5, SHA256, SSDEEP), ASCII/Unicode strings extraction, and PE timestamp auditing.", "intermediate", 3.5),
        ]),
        (25, "Phase 3: Defensive Engineering & Analysis", 3, "Malware Analysis & Reverse Engineering", 9, "Static and Dynamic Analysis", [
            ("static analysis workflow", "Safe sample intake, hashing, obfuscation checks, entropy calculation, and unpackers.", "advanced", 4.0),
            ("dynamic analysis workflow", "Executing samples in isolated virtual sandboxes, monitoring network and registry changes.", "advanced", 4.5),
            ("Ghidra introduction", "NSA Ghidra setup: decompilation, function graphs, data type definition, and cross-references.", "advanced", 5.0),
            ("x64dbg introduction", "Debugger setup: setting software/hardware breakpoints, stepping through assembly instructions.", "advanced", 5.0),
            ("PEStudio", "Rapid triage tool: inspecting indicators, suspicious imports, strings anomalies, and virusTotal API.", "intermediate", 3.5),
            ("Procmon and Process Explorer", "Sysinternals monitoring of live malware behavior, file modifications, and child processes.", "advanced", 4.5),
            ("safe malware-analysis lab methodology", "Building isolated host-only virtualization environments with snapshot recovery.", "intermediate", 3.5),
        ]),
        (26, "Phase 3: Defensive Engineering & Analysis", 3, "Malware Analysis & Reverse Engineering", 9, "Reverse Engineering Progression", [
            ("C for reverse engineering", "Mapping high-level C control structures (loops, structs, if-else) to compiled assembly.", "advanced", 4.0),
            ("assembly fundamentals", "x86/x64 assembly instructions (MOV, PUSH, POP, CALL, JMP), registers, and stack frames.", "advanced", 4.5),
            ("debugging concepts", "Hardware vs software breakpoints, memory stepping, register inspection, and patch creation.", "advanced", 4.5),
            ("reverse-engineering workflow", "Systematic code analysis: locating main entry point, analyzing critical functions, and bypassing checks.", "expert", 5.0),
            ("network behavior analysis with Wireshark", "Decoding malware C2 command-and-control beacons, DNS queries, and custom payloads.", "advanced", 4.5),
            ("document malware behavior", "Creating behavioral summary reports detailing persistence, capabilities, and IOC lists.", "advanced", 4.0),
            ("complete a safe sample-analysis report", "Conduct full static and dynamic analysis of a benign/crackme training binary.", "expert", 5.5),
        ]),

        # ── Phase 4: Trainer Engineering & Portfolio (Weeks 27–28) ───────────
        (27, "Phase 4: Trainer Engineering & Portfolio", 4, "Teaching and Trainer Systems", 10, "Teaching Systems", [
            ("beginner explanation techniques", "Analogies, scaffolding, cognitive load management, and non-technical language translation.", "intermediate", 3.5),
            ("professional explanation techniques", "Executive summaries, technical risk articulation, and business impact translation.", "intermediate", 3.5),
            ("live demo design", "Crafting reliable, fail-safe live demonstrations with backup recordings and clear takeaways.", "intermediate", 4.0),
            ("troubleshooting instruction", "Teaching debugging methodologies: binary search debugging, hypothesis testing, and error tracing.", "intermediate", 4.0),
            ("lab design", "Architecting reproducible, modular hands-on exercises with clear step-by-step verification points.", "intermediate", 4.0),
            ("quiz and assessment design", "Writing multiple-choice and scenario-based assessments with actionable diagnostic feedback.", "intermediate", 4.0),
            ("teach one complete networking/security lesson", "Record and self-evaluate a full 30-minute instructional session on a core security concept.", "advanced", 5.0),
        ]),
        (28, "Phase 4: Trainer Engineering & Portfolio", 4, "Teaching and Trainer Systems", 10, "Trainer Portfolio", [
            ("build a curriculum outline", "Develop a complete 4-week specialized course syllabus with objectives and prerequisites.", "advanced", 4.5),
            ("build one lab manual", "Write a complete student-facing lab manual with architecture diagrams and solution guides.", "advanced", 4.5),
            ("build one CTF challenge", "Design, build, and deploy an original capture-the-flag challenge with intentional vulnerability.", "expert", 5.5),
            ("create diagrams", "Design professional network and vulnerability flow diagrams using standard technical styling.", "intermediate", 4.0),
            ("create interview questions", "Compile 25 scenario-based cybersecurity technical interview questions with answer rubrics.", "intermediate", 4.0),
            ("create troubleshooting guides", "Author a comprehensive troubleshooting matrix for common network and operating system failures.", "intermediate", 4.0),
            ("assemble final Cybersecurity Trainer Portfolio", "Compile all instructional assets, lab guides, CTF challenges, and technical writeups into a production portfolio.", "expert", 6.0),
        ]),
    ]

    all_phases = {}
    
    current_day = 1
    
    for week_num, phase_name, phase_order, layer_name, layer_order, domain_name, days_info in weeks_blueprint:
        if phase_name not in all_phases:
            all_phases[phase_name] = {
                "name": phase_name,
                "order": phase_order,
                "description": f"Comprehensive roadmap segment for {phase_name}.",
                "skill_layers": {}
            }
        
        phase_dict = all_phases[phase_name]
        if layer_name not in phase_dict["skill_layers"]:
            phase_dict["skill_layers"][layer_name] = {
                "name": layer_name,
                "order": layer_order,
                "description": f"In-depth technical coverage of {layer_name}.",
                "estimated_days": 0,
                "domains": {}
            }
            
        layer_dict = phase_dict["skill_layers"][layer_name]
        if domain_name not in layer_dict["domains"]:
            layer_dict["domains"][domain_name] = {
                "name": domain_name,
                "order": len(layer_dict["domains"]) + 1,
                "description": f"Domain topics for {domain_name}.",
                "estimated_days": len(days_info),
                "topics": []
            }
            
        domain_dict = layer_dict["domains"][domain_name]
        layer_dict["estimated_days"] += len(days_info)
        
        for topic_idx, (title, desc, diff, hrs) in enumerate(days_info, start=1):
            topic_entry = {
                "name": f"Day {current_day} — {title.title()}",
                "description": desc,
                "order": topic_idx,
                "day_number": current_day,
                "estimated_hours": hrs,
                "difficulty": diff,
                "objectives": [
                    {
                        "description": f"Master core conceptual foundations of {title}.",
                        "order": 1,
                        "is_measurable": True
                    },
                    {
                        "description": f"Execute practical exercises and verify operational evidence for {title}.",
                        "order": 2,
                        "is_measurable": True
                    },
                    {
                        "description": f"Formulate defensive, troubleshooting, and teaching observations for Day {current_day}.",
                        "order": 3,
                        "is_measurable": True
                    }
                ]
            }
            domain_dict["topics"].append(topic_entry)
            current_day += 1

    # Convert nested dicts to serializable lists
    output_list = []
    for p_name, p_val in all_phases.items():
        phase_entry = {
            "name": p_val["name"],
            "order": p_val["order"],
            "description": p_val["description"],
            "skill_layers": []
        }
        for l_name, l_val in p_val["skill_layers"].items():
            layer_entry = {
                "name": l_val["name"],
                "order": l_val["order"],
                "description": l_val["description"],
                "estimated_days": l_val["estimated_days"],
                "domains": []
            }
            for d_name, d_val in l_val["domains"].items():
                layer_entry["domains"].append(d_val)
            phase_entry["skill_layers"].append(layer_entry)
        output_list.append(phase_entry)

    return output_list


def main():
    root_dir = Path(__file__).resolve().parent.parent.parent
    seeds_dir = root_dir / "backend" / "app" / "db" / "seeds"
    curriculum_dir = root_dir / "curriculum"
    
    seeds_dir.mkdir(parents=True, exist_ok=True)
    curriculum_dir.mkdir(parents=True, exist_ok=True)
    
    curriculum_data = get_all_196_days()
    
    # 1. Output backend seed file
    seed_file = seeds_dir / "curriculum_data.json"
    with open(seed_file, "w", encoding="utf-8") as f:
        json.dump(curriculum_data, f, indent=2)
    print(f"Generated seed file at {seed_file}")
    
    # 2. Output curriculum/roadmap.json and daily_tasks.json
    roadmap_file = curriculum_dir / "roadmap.json"
    with open(roadmap_file, "w", encoding="utf-8") as f:
        json.dump(curriculum_data, f, indent=2)
    print(f"Generated roadmap at {roadmap_file}")
    
    # Flatten daily tasks list
    daily_tasks = []
    total_days = 0
    for phase in curriculum_data:
        for layer in phase["skill_layers"]:
            for domain in layer["domains"]:
                for topic in domain["topics"]:
                    total_days += 1
                    daily_tasks.append({
                        "day_number": topic["day_number"],
                        "phase": phase["name"],
                        "skill_layer": layer["name"],
                        "domain": domain["name"],
                        "topic": topic["name"],
                        "description": topic["description"],
                        "estimated_hours": topic["estimated_hours"],
                        "difficulty": topic["difficulty"],
                        "objectives": [obj["description"] for obj in topic["objectives"]]
                    })
                    
    daily_tasks_file = curriculum_dir / "daily_tasks.json"
    with open(daily_tasks_file, "w", encoding="utf-8") as f:
        json.dump(daily_tasks, f, indent=2)
    print(f"Generated daily tasks at {daily_tasks_file}")
    print(f"Total days verified: {total_days} / 196")


if __name__ == "__main__":
    main()
