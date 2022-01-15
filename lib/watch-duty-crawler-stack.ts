import { Stack, StackProps, aws_lambda_nodejs } from 'aws-cdk-lib';
import { Construct } from 'constructs';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class WatchDutyCrawlerStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const func = new aws_lambda_nodejs.NodejsFunction(this, "crawler")

    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, 'WatchDutyCrawlerQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });
  }
}
