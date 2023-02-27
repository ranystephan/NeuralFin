import Header_News from '../../components/Header_News'





const styles = {
  wrapper: "w-screen h-screen flex flex-col",


}

export default function Home() {
  return (
    <div className={styles.wrapper}>
      <Header_News />
    </div>


  )
}
