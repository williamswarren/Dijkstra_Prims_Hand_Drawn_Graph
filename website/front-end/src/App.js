import React, {Component} from 'react';
import monkey from './monkey.png';
import styled, { keyframes } from "styled-components";
import { flip } from 'react-animations';
import axios from 'axios';

const FlipAnimation = keyframes`${flip}`;
const FlipDiv = styled.div`
  animation: infinite 2s ${FlipAnimation};
  top: 35%;
  left: 40%;
  display: flex;
  justify-content: center;
  position: absolute;
`;


class App extends Component {
    state = { selectedFile: null,
				image1: null,
				image2: null,
				image3: null,
				ajacency_list: null,
				error: false};


	onFileChange = (event) => {
		const file = event.target.files[0]
		this.setState({selectedFile: file});
		console.log(event)
		console.log(this.state)
			
		let data = new FormData();
		data.append('graph_image', file);
		
		axios.post('http://ec2-3-101-117-97.us-west-1.compute.amazonaws.com:3000',
  			data)
		.then((response) => {
			console.log("Response");
  			console.log(response);

			if (Object.keys(response.data).length != 4){
					this.setState({error: true, 
                    selectedFile: null});}
			else{
			this.setState({image1: new Buffer.from(response.data.image1).toString("base64"),
						image2: new Buffer.from(response.data.image2).toString("base64"),
						image3: new Buffer.from(response.data.image3).toString("base64"),
						adjacency_list: new Buffer.from(response.data.adjacency_list).toString()})
		}}, (error) => {
  		console.log(error);
		this.setState({error: true, 
					selectedFile: null});
		});

}	
	
	processing = () => {
		if (this.state.selectedFile){
			if (this.state.image1){return (null)}
    	return(
		<div>
    		<FlipDiv> <img className='image' src={monkey} /> </FlipDiv>
			<label style={{top:"50% !important", position: "absolute", display:"flex", margin: "-150px 0 0 20px"}}> LOADING (THIS WILL TAKE A LITTLE BIT) </label>
		</div>
    	);}
    	else{
    	return(
    	<div>
        	<img className='image' src={monkey} />
        	<label style={{top:"50% !important", position: "absolute", display:"flex", margin: "-150px 0 0 300px"}}> UPLOAD PNG 
            	<input type="file" name="file" onChange={this.onFileChange} />
        	</label>
    	</div>
    	);}
}


	result = () => {
		if (this.state.image1 && this.state.image2 && this.state.image3){
			return(
			<div>
				<div className='row'>
					<div className='column'>
						<img width='300' height='300' src={'data:image/png;base64,' + this.state.image1}/>
						<a download="graphviz-image.png" href={'data:image/png;base64,' + this.state.image1} > GRAPHVIZ IMAGE </a>
					</div>
					<div className='column'>
						<img width='300' height='300' src={'data:image/png;base64,' + this.state.image2}/>
						<a download="processed-image.png" href={'data:image/png;base64,' + this.state.image2} > PROCESSED IMAGE </a>
					</div>
					<div className='column'>
						<img width='300' height='300' src={'data:image/png;base64,' + this.state.image3}/>
						<a download="nodes_weights.png" href={'data:image/png;base64,' + this.state.image3} > NODES & WEIGHTS </a>
					</div>
				</div>
				<div>
					<p>ADJACENCY LIST > {this.state.adjacency_list}</p>
				</div>
			</div>)}
		else if(this.state.error == true){
			return(<label style={{top:"50% !important", position: "absolute", display:"flex", margin: "-30px 0 0 -80px", color: 'red', fontFamily: "arial", fontWeight: "bold", fontSize: "30px"}}> SORRY SOMETHING WENT WRONG :( PLEASE TRY AGAIN WITH A DIFFERENT IMAGE </label>

)}

}
	

    render() {
		console.log(this.state.selectedFile)
      return (
		<div>
        	<h> GRAPHMONKEY</h>
			{this.processing()}
			{this.result()}
		</div>
     );
   }
 }

export default App;
