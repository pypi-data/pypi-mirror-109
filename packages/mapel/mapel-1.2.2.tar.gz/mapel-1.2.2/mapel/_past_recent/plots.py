#!/usr/bin/env python

import mapel
import matplotlib.pyplot as plt


if __name__ == "__main__":


        pis = [pow(x,2)/pow(20,2) for x in range(0, 20)]
        po = [pow(1.2,x)/pow(1.2,20) for x in range(0,20)]
        plt.plot(pis, label='x^3')
        plt.plot(po, label='1.1^x')
        plt.legend()
        plt.savefig("tmp_plot")
        plt.show()


        # widelki = ["10%", "20%", "30%", "40%", "50%"]
        # pis = [32,33,35,35,36]
        # po = [33,34,35,36,37]
        #
        # plt.plot(widelki, pis, marker='o', label="PiS")
        # plt.plot(widelki, po, marker='o', label="PO")
        # plt.legend()
        # plt.ylabel("Liczba mandatów")
        # plt.xlabel("Maksymalne odchylenia wielkości okręgów")
        # plt.savefig("plot_1")
        # plt.show()
        #
        # widelki = ["1.10", "1.08", "1.06", "1.04", "1.02", "1.00"]
        # pis = [33,34,34,35,35,36]
        # po = [33,34,34,35,36,37]
        #
        # plt.plot(widelki, pis, marker='o', label="PiS")
        # plt.plot(widelki, po, marker='o', label="PO")
        # plt.legend()
        # plt.ylabel("Liczba mandatów")
        # plt.xlabel("Wspołczynnik wygranej")
        # plt.savefig("plot_2")
        # plt.show()