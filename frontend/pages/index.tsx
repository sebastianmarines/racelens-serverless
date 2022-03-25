import { useState } from "react";
import type { NextPage } from "next";
import Head from "next/head";
import Image from "next/image";
import styles from "../styles/Home.module.css";
import { authStore } from "../lib/authStore";

import { Amplify } from "aws-amplify";
import { signIn } from "../lib/auth";

Amplify.configure({
  // TODO: Variable configuration
  Auth: {
    userPoolId: "us-east-1_ZIWUjWNqs", //UserPool ID
    region: "us-east-1",
    userPoolWebClientId: "6js8lq5ro8bkl64u4sgarsaedb", //WebClientId
  },
});

const Home: NextPage = () => {
  const [state, setState] = useState({
    email: "",
    password: "",
  });

  const userName = authStore((state) => state.user.name);
  const token = authStore((state) => state.token);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setState({ ...state, [name]: value });
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await signIn(state.email, state.password);
  };

  return (
    <div className={styles.container}>
      <Head>
        <title>Create Next App</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to <a href="https://nextjs.org">Next.js!</a>
        </h1>
        <h2>Hello {userName}</h2>
        {userName ? (
          <div></div>
        ) : (
          <form onSubmit={handleSubmit}>
            <label htmlFor="email">Email</label>
            <input
              type="text"
              name="email"
              id="email"
              onChange={handleChange}
            />
            <label htmlFor="password">Password</label>
            <input
              type="password"
              name="password"
              id="password"
              onChange={handleChange}
            />
            <button type="submit">Submit</button>
          </form>
        )}
      </main>
      <footer className={styles.footer}>
        <a
          href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          Powered by{" "}
          <span className={styles.logo}>
            <Image src="/vercel.svg" alt="Vercel Logo" width={72} height={16} />
          </span>
        </a>
      </footer>
    </div>
  );
};

export default Home;
