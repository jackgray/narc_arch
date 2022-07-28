import type { NextPage } from 'next'
import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'

const Home: NextPage = () => {
  return (
    <div className={styles.container}>
      <Head>
        <title>NARC Lab Dashboard</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to the NARC lab dashboard!
        </h1>

        <p className={styles.description}>
          This page is under construction{' '}
          {/* <code className={styles.code}>pages/index.tsx</code> */}
        </p>

        <div className={styles.grid}>
          <a href="data" className={styles.card}>
            <h2>Database &rarr;</h2>
            <p>Connect with the Arango DB client directly</p>
          </a>

          <a href="vms" className={styles.card}>
            <h2>Virtual Machines &rarr;</h2>
            <p>Select a data path to mount and spin up a virtual machine powered by the cluster</p>
          </a>

          <a
            href="projects"
            className={styles.card}
          >
            <h2>Projects &rarr;</h2>
            <p>Connect with Leantime, the open-source project-tracking client.</p>
          </a>

          <a
            href="jobs.narclab.com"
            className={styles.card}
          >
            <h2>Jobs &rarr;</h2>
            <p>
              Check on the status of your job submissions
            </p>
          </a>
        </div>
      </main>

      <footer className={styles.footer}>
        <a
          href="narclab2022"
          target="_blank"
          rel="noopener noreferrer"
        >
          Powered by{' '}
          <span className={styles.logo}>
            <Image src="/sinailogo.png" alt="Mount Sinai" width={72} height={16} />
          </span>
        </a>
      </footer>
    </div>
  )
}

export default Home