delay_examples = [
    {
        'description': 'The average delay of a transatlantic connection',
        'value': 100,
    }, {
        'description': 'The average delay of a connection within the EU or the US',
        'value': 35,
    }, {
        'description': 'A satellite modem in the woods (terrible!)',
        'value': 600,
    }
]

loss_examples = [
    {
        'description':
        'A wifi connection on the same channel as all your neighbours in an densely populated apartment building',
        'value':
        "10",
    },
    {
        'description': 'Packet loss high enough for streamed video/voip to have problems',
        'value': "7.5",
    },
    {
        'description': 'A fairly high packet loss rate under which things should still work.',
        'value': "2.5",
    },
]

duplication_examples = [
    {
        'description':
        'Two switches misconfigured to broadcast the same traffic to the same address ',
        'value': "100",
    },
    {
        'description': 'Duplication due to high packet loss causing dropped ACKs',
        'value': "5",
    },
    {
        'description': 'Duplication due to minor packet loss causing dropped ACKs',
        'value': "2",
    },
]

reordering_examples = [
    {
        'description': 'Some packets taking a slower path through the network',
        'ms': 100,
        'percent': "5",
    },
    {
        'description': 'Many packets taking an almost as good path through the network',
        'ms': 10,
        'percent': "50",
    },
]

corruption_examples = [
    {
        'description': 'DSL Modem with degrading filter',
        'value': "1",
    }, {
        'description': 'Poorly shielded cable next to an EMI source',
        'value': "5"
    }
]

rate_examples = [
    {
        'description': 'A dialup modem',
        'kbit': 56,
        'latency': 1000,
        'burst': 10000,
    }, {
        'description': 'A slow ADSL connection',
        'kbit': 1536,
        'latency': 1000,
        'burst': 10000,
    }, {
        'description': 'A standard ADSL connection',
        'kbit': 4096,
        'latency': 1000,
        'burst': 10000,
    }, {
        'description': 'The max throughput of udp over 802.11b wifi',
        'kbit': 7270,
        'latency': 1000,
        'burst': 10000,
    }
]
